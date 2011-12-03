from paste.httpserver import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

import logging
import random
import os

import markov
import string

log = logging.getLogger(__name__)

Markov = markov.Letters(3)

randbool = lambda: random.choice([True, False])
bool_param = lambda request, param: bool(request.GET.get(param, 'N') in 'Yy')
int_param = lambda request, param, default: int(request.GET.get('number', default))

def mkpasswd(add_number=True, alternate_case=True, add_punctuation=True):
    word = Markov.generate(random.randint(6,10))
    
    if alternate_case:
        word = ''.join(i.upper() if randbool() else i for i in word)

    if add_punctuation:
        pos = random.randint(0, len(word))
        word = word[:pos] + random.choice(string.punctuation) + word[pos:]

    if add_number:
        num_fmts = [ ('%02d', 100), ('%03d', 1000) ]
        fmt, upper = random.choice(num_fmts)

        num = fmt % random.randint(0, upper)
        pos = random.randint(0, len(word))
        word = word[:pos] + num + word[pos:]

    return word

@view_config(route_name='words', renderer='json')
def words(request):

    number = min(int_param(request, 'number', 100), 1000)

    add_number = bool_param(request, 'add_number')
    add_punctuation = bool_param(request, 'add_punctuation')
    alternate_case = bool_param(request, 'alternate_case')

    def passwd():
        return mkpasswd(add_number=add_number,
                        add_punctuation=add_punctuation,
                        alternate_case=alternate_case)

    words = [ passwd() for i in range(number) ]
    return {'words': words}

@view_config(route_name='root', renderer='root.mako')
def root(request):
    return {}

def main(global_config, **settings):

    if os.path.exists('/tmp/markov.data'):
        log.info('Loading markov training')

        Markov.load('/tmp/markov.data')
    else: 
        log.info('Training markov...')

        Markov.process('/usr/share/dict/words')
        Markov.normalize()
        Markov.dump('/tmp/markov.data')

        log.info('Training complete')

    config = Configurator(settings=settings)
    config.add_route('root', '/')
    config.add_route('words', '/words')
    config.add_static_view('static', 'passwd:static')
    config.scan()

    return config.make_wsgi_app()

if __name__ == '__main__':    
    serve(main(), host='0.0.0.0')
