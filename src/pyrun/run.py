import sys
from vm import VirtualMachine

def main():
    filename = sys.argv[1]

    with open(filename, 'r') as file:
        source = file.read()
    
    code = compile(source, filename, 'exec')

    vm = VirtualMachine()
    vm.run_code(code)

if __name__ == '__main__':
    main()