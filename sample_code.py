#! /usr/bin/python3

import sys

def alpha():
    print('alpha')

def delta():
    print('delta')

class Beta:
    def __init__(self):
        print('beta init')

    def charlie(self):
        print('charlie')
        delta()

class Foxtrott ( Beta ):
    pass

def main():
    print('main')
    alpha()
    beta=Beta()
    beta.charlie()
    echo=Beta()
    echo.charlie()
    foxtrott=Foxtrott()
    foxtrott.charlie()

alpha()

print('Sample name', __name__, 'argv: ', sys.argv)

if __name__== "__main__":
    main()
