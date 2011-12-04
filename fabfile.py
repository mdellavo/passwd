
from fabric.api import *

APP_NAME = 'passwd.quuux.org'
GIT_ORIGIN = 'git://github.com/mdellavo/passwd.git'

ENV_DIR = '/var/www/' + APP_NAME
SRC_DIR = ENV_DIR + '/src'
ETC_DIR = ENV_DIR + '/etc'
RUN_DIR = ENV_DIR + '/run'
LOG_DIR = ENV_DIR + '/log'

def virtualenv_activate(env):
    return prefix('source %s/bin/activate' % env)

def deploy():
    with settings(warn_only=True):
        if run('test -d %s' % ENV_DIR).failed:
            sudo('virtualenv --no-site-packages %s' % ENV_DIR) 
            sudo('git clone %s %s' % (GIT_ORIGIN, SRC_DIR))

            with cd(SRC_DIR):
                sudo('mkdir %s' % ETC_DIR)
                sudo('mkdir %s' % RUN_DIR)
                sudo('mkdir %s' % LOG_DIR)
                sudo('cp -f uwsgi.ini /etc/uwsgi-python/apps-available/%s.ini' % \
                        APP_NAME)
                sudo(('ln -sf /etc/uwsgi-python/apps-available/%s.ini ' \
                        '/etc/uwsgi-python/apps-enabled/%s.ini') % \
                        (APP_NAME, APP_NAME))

    with cd(SRC_DIR):
        sudo('git pull')

        with virtualenv_activate(ENV_DIR):
            sudo('pip install -U -r requirements.txt')
            sudo('python setup.py install')

        sudo('cp production.ini %s' % ETC_DIR)
        sudo('touch %s/reload' % RUN_DIR)
        
        
