""" This program is a simple yes/no parser.
The program should read a text file that contains a program for the robot, and
verify whether the syntax is correct.
You must verify that used function names and variable names have been previously
defined or in the case of functions, that they are the function’s arguments. You must
allow recursion.
Spaces and tabulators are separators and should be ignored (outside of instructions)."""

import re

name_pattern = r'\w+[\w\d]*'
var_pattern = rf'^\s*VAR(\s*{name_pattern},)*\s*{name_pattern};$'
# exp = rf'^(PROG|prog)[\s\n]*{var_pattern}\n*'

def main():
    greatbool = False
    code = open("Prueba.txt", "r")
    code = code.read()
    code = code.strip()

    # parse(code)
    # Verify if the code starts with PROG and ends with GORP.
    if (code[:4]) == "PROG" and (code[-4:]) == "GORP":
        code = code[4:]
        code = code[:-4]
        greatbool = parse(code)

    # print(greatbool)

def parse(code):
    # Parsea el codigo
    # code = whitecode(code)
    code2 = code.splitlines()
    variables = []
    parameters = []
    # print(code)
    # codigo = re.match(re.compile(exp), code)
    # print(codigo, 'a')
    in_procedure = False
    for line in code2:
        is_var, variables_temp = declareVariables(line)
        if is_var:
            variables = variables_temp

        is_procedure, parameters_temp = checkProcedure(line)

        if is_procedure:
            in_procedure = True
            parameters = parameters_temp

        # checkIns(line)

        if in_procedure:
            checkCommand(line, parameters, variables)
        checkAssignment(line)

def declareVariables(line):
    # Revisa las declaraciones de variables
    is_match = re.match(re.compile(var_pattern), line)
    lista_variables = None

    if is_match is not None:
        line = line.strip('VAR ')
        line = line.strip(';')
        lista_variables = line.split(', ')

    return is_match, lista_variables

def checkProcedure(line):
    # Revisa si la definición de un Procedimiento es válida
    proc_pattern = re.compile(rf'^\s*PROC\s*{name_pattern}\s*\(((({name_pattern},)*\s*{name_pattern}\))|\s*\))$')
    parameter_pattern = re.compile(rf'\(({name_pattern},)*\s*{name_pattern}\)')
    parameters = []

    is_procedure = re.match(proc_pattern, line)
    if is_procedure is not None:
        parameters = re.search(parameter_pattern, line)
        if parameters is not None:
            parameters = parameters.group(0)
            parameters = parameters.strip('() ')
            parameters = parameters.split(', ')
        else:
            parameters = []
    return (bool(is_procedure), parameters)

def checkIns(line):
    pass

def checkCommand(line, parameters, variables):
    commandslist = ["walk", "jump", "drop", "grab", "get", "free", "pop"]
    orientationList = ["north", "south", "east", "west"]
    directionsList = ["around", "left", "right"]
    walkList = orientationList.copy()
    walkList.extend(["front", "back", "left", "right"])


    commands = '|'.join(commandslist)
    posibles = variables.copy()
    posibles.extend(parameters)
    posibles_parameters = '|'.join(posibles)
    posibles_orientation = '|'.join(orientationList)
    posibles_directions = '|'.join(directionsList)
    posibles_walks = '|'.join(walkList)


    command_pattern = re.compile(rf'^\s*({commands})\s*\(\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$')
    jumpTo_pattern = re.compile(rf'^\s*jumpTo\s*\(\s*(({posibles_parameters})|\d+)\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$')
    veer_pattern = re.compile(rf'^\s*veer\s*\(\s*({posibles_directions})\s*\)\s*;\s*$')
    look_pattern = re.compile(rf'^\s*look\s*\(\s*({posibles_orientation})\s*\)\s*;\s*$')
    walk_pattern = re.compile(rf'^\s*walk\s*\(\s*({posibles_walks})\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$')

    is_command = re.match(command_pattern, line)
    is_jumpTo = re.match(jumpTo_pattern, line)
    is_veer = re.match(veer_pattern, line)
    is_look = re.match(look_pattern, line)
    is_walk = re.match(walk_pattern, line)

    if is_command is not None:
        print(is_command.group(0))

    if is_jumpTo is not None:
        print(is_jumpTo.group(0))

    if is_veer is not None:
        print(is_veer.group(0))

    if is_look is not None:
        print(is_look.group(0))

    if is_walk is not None:
        print(is_walk.group(0))

def checkAssignment(line):
    assign_pattern = re.compile(rf'^\s*({name_pattern})\s*:=\s*\d+\s*;$')
    is_match = re.match(assign_pattern, line)
    if is_match is not None:
        print(is_match.group(0))

if __name__ == '__main__':
    main()



# ["isfacing", "isValid", "canWalk, "not"]
