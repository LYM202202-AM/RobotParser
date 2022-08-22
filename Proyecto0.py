#!/usr/bin/python3
""" This program is a simple yes/no parser.
The program should read a text file that contains a program for the robot, and
verify whether the syntax is correct.
You must verify that used function names and variable names have been previously
defined or in the case of functions, that they are the function’s arguments. You must
allow recursion.
Spaces and tabulators are separators and should be ignored (outside of instructions)."""

import re

name_pattern = r'\w+[\w\d]*'
var_pattern = rf'^\s*(var|VAR)(\s*{name_pattern},)*\s*{name_pattern};$'
exp = rf'^(PROG|prog)[\s\n]*{var_pattern}\n*'

def main():
    greatbool = False
    code = open("prueba2.txt", "r")
    code = code.read()
    code = code.strip()

    parse(code)
    # Verify if the code starts with PROG and ends with GORP.
    # if (code[:4]) == "PROG" and (code[-4:]) == "GORP":
    #     code = code[4:]
    #     code = code[:-4]
    #     greatbool = parse(code)

    # print(greatbool)

def parse(code):
    # Parsea el codigo
    # code = whitecode(code)
    code2 = code.splitlines()
    print(code)
    codigo = re.match(re.compile(exp), code)
    print(codigo, 'a')
    for line in code2:
        variables = declareVariables(line)
        if variables is not None:
            print(variables)

        checkProcedure(line)


def whitecode(code):
    # Filtra el codigo con caracteres válidos
    """whitelist = set('abcdefghijklmnopqrstuvwxyz{[()]}/-,;ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    code = ''.join(filter(whitelist.__contains__, code)) """
    code = code.replace("\n", "")
    code = code.replace("{", "{;")
    code = code.replace("}", "};")
    code = code.split(";")
    return code

def declareVariables(line):
    # Revisa las declaraciones de variables
    is_match = re.match(re.compile(var_pattern), line)

    if is_match is not None:
        line = line.strip('var ')
        line = line.strip('VAR ')
        line = line.strip(';')
        lista_variables = line.split(', ')
        return lista_variables

def checkProcedure(line):
    # Revisa si la definición de un Procedimiento es válida
    proc_pattern = re.compile(rf'^\s*(PROC|proc)\s*{name_pattern}\s*\(((({name_pattern},)*\s*{name_pattern}\))|\s*\))')
    is_match = re.match(proc_pattern, line)
    return bool(is_match)

if __name__ == '__main__':
    main()
