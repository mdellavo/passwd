import re
import random
import sys
import pprint
import os
import getopt
import string

class Markov(object):
    join_str = ''

    def __init__(self, order=2):
        self.order      = order
        self.dist       = {}

    def process(self, input):
        for group in self.groups(input):
            last = group[:-1]
            self.dist[last] = self.dist.get(last, {})
            self.dist[last][group[-1]] = self.dist[last].get(group[-1], 0) + 1

    def normalize(self):
        for i in self.dist:
            num = float(sum(self.dist[i].values()))

            for j in self.dist[i]:
                self.dist[i][j] = float(self.dist[i][j]) / num

    def dump(self, path):
        f = open(path, 'w')
        pprint.pprint(self.dist, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        self.dist = eval(f.read())
        f.close()

    def groups(self, input):
        group = []

        for atom in self.atoms(input):
            if not atom:
                group = []
                continue

            group.append(atom)

            if len(group) == self.order:
                yield tuple(group)
                group = group[1:]

    def walk(self, length):
        current_group = list(random.choice(self.dist.keys()))

        for i in range(length):
            j = tuple(current_group)

            while j not in self.dist:
                current_group = list(random.choice(self.dist.keys()))
                j = tuple(current_group)
            
            selected = random.random()
            total    = 0.0

            for k,v in self.dist[j].items():
                total += v

                if selected < total:
                    next_atom = k
                    break

            current_group.append(next_atom)
            current_group = current_group[1:]

            yield next_atom

    def generate(self, length):
        return self.join_str.join([ i for i in self.walk(length) ])

class Text(Markov):
    join_str      = ' '
    split_pattern = re.compile(r'[^\w\']+')

    def atoms(self, input):
        for line in input:
            for word in self.split_pattern.split(line):
                if word:
                    yield word.lower()

            yield None

class Letters(Markov):
    split_pattern = re.compile(r'[^a-zA-Z]+')
    
    def atoms(self, input):
        for line in input:
            for word in self.split_pattern.split(line):
                if word:
                    for char in word:
                        yield char.lower()

                    yield None

if __name__ == '__main__':

    markov = Letters(3)
    
    markov.process(open('/usr/share/dict/words'))
    markov.normalize()
       
    def mkpasswd():
        word = markov.generate(random.randint(6,10))
        num_fmts = [ ('%02d', 100), ('%03d', 1000) ]

        fmt, upper = random.choice(num_fmts)
        num =  fmt % random.randint(0, upper)

        return word + num

    word_length = 6
    test_size = 10000
    test = set(mkpasswd() for i in range(test_size))

    for i in test:
        print i

    print
    print 'word_length =', word_length    
    print 'test_size =', test_size
    print 'len(test) =', len(test)

    print 'collision_rate =', (1 - float(len(test))/test_size) * 100

