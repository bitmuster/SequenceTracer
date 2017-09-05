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
        alpha()
    def charlie(self):
        print('charlie')
        delta()


def main():
    print('main')
    alpha()
    beta=Beta()
    beta.charlie()

if __name__== "__main__":
    # does not work as the name is sample_code when called from sequence tracer
    main() 

print('Name', __name__)
main()

