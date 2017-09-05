#! /usr/bin/python3

def alpha():
    print('alpha')
    pass

def delta():
    print('delta')
    pass

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

if __name__== "__main__":
    # does not work as the name is sample_code when called from sequence tracer
    main() 

print('Name', __name__)
main()

