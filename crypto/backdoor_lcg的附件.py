import os
import hashlib
from string import ascii_letters
from Crypto.Util.number import *
from Crypto.Random.random import randrange, getrandbits, choice

from flag import flag

banner = '''welcome to llcg1'''


class LCG(object):
    def __init__(self, seed):
        self.N = getPrime(256)
        self.a = randrange(self.N)
        self.b = randrange(self.N)
        self.seed = seed % self.N
        self.state = self.seed

    def next(self):
        self.state = (self.a * self.state + self.b) % self.N
        return self.state

def challenge1():
    print('-------------------question1----------------------')

    init_seed = getrandbits(256)
    lcg = LCG(init_seed)
    print('N = ' + str(lcg.N))
    print('a = ' + str(lcg.a))
    print('b = ' + str(lcg.b))
    print('lcg.next() = ' + str(lcg.next()))

    guess = int(input("lcg.seed = "))
    if guess != lcg.seed:
        print('you are wrong, exit...')
        exit(0)


def challenge2():
    print('-------------------question2----------------------')
    init_seed = getrandbits(256)
    lcg = LCG(init_seed)
    print('N = ' + str(lcg.N))
    print('a = ' + str(lcg.a))
    print('lcg.next() = ' + str(lcg.next()))
    print('lcg.next() = ' + str(lcg.next()))
    guess = int(input("lcg.seed = "))
    if guess != lcg.seed:
        print('you are wrong, exit...')
        exit(0)


def challenge3():
    print('-------------------question3----------------------')
    init_seed = getrandbits(256)
    lcg = LCG(init_seed)
    print('N = ' + str(lcg.N))
    print('lcg.next() = ' + str(lcg.next()))
    print('lcg.next() = ' + str(lcg.next()))
    print('lcg.next() = ' + str(lcg.next()))
    guess = int(input("lcg.seed = "))
    if guess != lcg.seed:
        print('you are wrong, exit...')
        exit(0)


def challenge4():
    print('-------------------question4----------------------')

    init_seed = getrandbits(256)
    lcg = LCG(init_seed)
    for _ in range(6):
        print('lcg.next() = ' + str(lcg.next()))
    guess = int(input("lcg.seed = "))
    if guess != lcg.seed:
        print('you are wrong, exit...')

        exit(0)
    print('Here is your flag: ' + flag)



if __name__ == '__main__':
    try:
        challenge1()
        challenge2()
        challenge3()
        challenge4()
    except:
        exit(0)
