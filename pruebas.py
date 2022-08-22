import re

def main():
    code = open("prueba3.txt", "r")
    code = code.read()
    code = code.replace('{', '[')
    code = code.replace('}', ']')

    commandslist = ["walk", "jump", "drop", "grab", "get", "free", "pop"]
    commandslist2 = ["jumpTo"]

    commands = '|'.join(commandslist)
    posibles = ['n', 'x', 'y', 'c', 'b']
    posibles_parameters = '|'.join(posibles)


    command_pattern = rf'({commands})\s*\(({posibles_parameters})\s*\)'

    instructions = rf'[\s\n]*\[\n+[\s\n]*({command_pattern};[\n\s]*)+({command_pattern})[\n\s]*\]'
    is_present = re.search(re.compile(instructions), code)

    if is_present is not None:
        print(is_present.group())

if __name__ == "__main__":
    main()