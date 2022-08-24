""" This program is a simple yes/no parser.
The program should read a text file that contains a program for the robot, and
verify whether the syntax is correct.
You must verify that used function names and variable names have been previously
defined or in the case of functions, that they are the function’s arguments. You must
allow recursion.
Spaces and tabulators are separators and should be ignored (outside of instructions)."""

import re
from signal import valid_signals

name_pattern = r'\w+[\w\d]*'
var_pattern = rf'^\s*VAR(\s*{name_pattern},)*\s*{name_pattern};$'
# exp = rf'^(PROG|prog)[\s\n]*{var_pattern}\n*'

commandslist = ["walk", "jump", "drop", "grab", "get", "free", "pop"]
orientationList = ["north", "south", "east", "west"]
directionsList = ["around", "left", "right"]
walkList = orientationList.copy()
walkList.extend(["front", "back", "left", "right"])


commands = '|'.join(commandslist)
posibles_orientation = '|'.join(orientationList)
posibles_directions = '|'.join(directionsList)
posibles_walks = '|'.join(walkList)


def main():
    greatbool = False
    code = open("Prueba.txt", "r")
    code = code.read()
    code = code.replace('{', '[')
    code = code.replace('}', ']')
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
        checkCondition(line, parameters, variables)

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

    posibles = variables.copy()
    posibles.extend(parameters)
    posibles_parameters = '|'.join(posibles)

    command_pattern = rf'^\s*({commands})\s*\(\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$'
    jumpTo_pattern = rf'^\s*jumpTo\s*\(\s*(({posibles_parameters})|\d+)\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$'
    veer_pattern = rf'^\s*veer\s*\(\s*({posibles_directions})\s*\)\s*;\s*$'
    look_pattern = rf'^\s*look\s*\(\s*({posibles_orientation})\s*\)\s*;\s*$'
    walk_pattern = rf'^\s*walk\s*\(\s*({posibles_walks})\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*;\s*$'
    assign_pattern = rf'^\s*({name_pattern})\s*:=\s*\d+\s*;$'

    global_command_pattern = rf'({command_pattern}|{jumpTo_pattern}|{veer_pattern}|{look_pattern}|{walk_pattern}|{assign_pattern})'

    is_match = re.match(global_command_pattern, line)
    if is_match is not None:
        print(is_match.group(0))


def checkIf(line, parameters, variables):
    pass
    # if_pattern = re.compile(rf'^\s*if\s*({condition})')

def checkCondition(line, parameters, variables):

    posibles = variables.copy()
    posibles.extend(parameters)
    posibles_parameters = '|'.join(posibles)


    validList = ["walk", "jump", "grab", "pop" "pick", "free", "drop"]
    canWalkList = ["north", "south", "east", "west", "front", "back", "left", "right"]

    posibles_valid = '|'.join(validList)
    posibles_canWalk = '|'.join(canWalkList)

    facing_pattern = rf'\s*isfacing\s*\(\s*({posibles_orientation})\s*\)\s*'
    isvalid_pattern = rf'\s*isValid\s*\(\s*({posibles_valid})\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*'
    canwalk_pattern = rf'\s*canWalk\s*\(\s*({posibles_canWalk})\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*'


    condition_pattern = rf'\s*({facing_pattern}|{isvalid_pattern}|{canwalk_pattern})\s*'

    not_pattern = rf'\s*not\s*\(\s*({condition_pattern})\s*\)\s*'

    global_condition_pattern = rf'\s*({condition_pattern}|{not_pattern})\s*'

    command_pattern = rf'\s*({commands})\s*\(\s*(({posibles_parameters})|\d+)\s*\)\s*'
    jumpTo_pattern = rf'\s*jumpTo\s*\(\s*(({posibles_parameters})|\d+)\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*'
    veer_pattern = rf'\s*veer\s*\(\s*({posibles_directions})\s*\)\s*'
    look_pattern = rf'\s*look\s*\(\s*({posibles_orientation})\s*\)\s*'
    walk_pattern = rf'\s*walk\s*\(\s*({posibles_walks})\s*,\s*(({posibles_parameters})|\d+)\s*\)\s*'
    assign_pattern = rf'\s*({posibles_parameters})\s*:=\s*\d+\s*'

    global_command_pattern = rf'({command_pattern}|{jumpTo_pattern}|{veer_pattern}|{look_pattern}|{walk_pattern}|{assign_pattern})'


    if_pattern = rf'^\s*if\s*\(({global_condition_pattern})\)\s*\[\s*{global_command_pattern}\s*\]\s*(else\s*\[{global_command_pattern}\])?\s*fi\s*'

    is_match = re.search(if_pattern, line)
    if is_match is not None:
        print(is_match.group(0))
if __name__ == '__main__':
    main()



# ["isfacing", "isValid", "canWalk, "not"]
