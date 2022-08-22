#!/usr/bin/python3
""" This program is a simple yes/no parser.
The program should read a text file that contains a program for the robot, and
verify whether the syntax is correct.
You must verify that used function names and variable names have been previously
defined or in the case of functions, that they are the function’s arguments. You must
allow recursion.
Spaces and tabulators are separators and should be ignored (outside of instructions)."""

import re

def main():
    greatbool = False
    code = open("Prueba.txt", "r")
    code = code.read()
    code = code.strip()

    # Verify if the code starts with PROG and ends with GORP.
    if (code[:4]) == "PROG" and (code[-4:]) == "GORP":
        code = code[4:]
        code = code[:-4]
        greatbool = parse(code)

    print(greatbool)

def parse(code):
    # Parsea el codigo
    parenthesis = code.count("(") == code.count(")")
    brackets = code.count("{") == code.count("}")

    if parenthesis and brackets:
        # code = whitecode(code)
        code = code.splitlines()
        for line in code:
            name_pattern = r'\w+(\w\d)*'
            var_pattern = re.compile(rf'^\s*(var|VAR)(\s*{name_pattern},)*\s*{name_pattern};$')
            is_match = re.match(var_pattern, line)
            if is_match is not None:
                print(is_match.group(0))

    """     greatbool = True
    declarPROC = False

    for line in code:
        if greatbool:
            if line[:3] == "var":
                greatbool = checkVariables(line, greatbool)
            elif line[:4] == "PROC":
                greatbool = checkProcedure(line, greatbool)
                declarPROC = greatbool
            elif declarPROC and line != "while":
                commandslist = ["walk", "jump", "jumpTo", "veer", "look", "drop", "grab", "get", "free", "pop", "walk"]
                for command in commandslist:
                    if command in line:
                        boolx = True
                        line = line.replace(command, "")
                        if not "(" in line or not ")" in line:
                            boolx = False
                        else:
                            whitelist = set('abcdefghijklmnopqrstuvwxyz/-,;ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                            line = ''.join(filter(whitelist.__contains__, line))
                            line = line. split(";")
                            print(line)
                            # for paramenter in line:
                                # if paramenter ==

            # if counter != 0:
                #     line[counter:]"""



def whitecode(code):
    # Filtra el codigo con caracteres válidos
    """whitelist = set('abcdefghijklmnopqrstuvwxyz{[()]}/-,;ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    code = ''.join(filter(whitelist.__contains__, code)) """
    code = code.replace("\n", "")
    code = code.replace("{", "{;")
    code = code.replace("}", "};")
    code = code.split(";")
    return code

def checkVariables(line, greatbool):
    # Revisa las declaraciones de variables
    line = line[3:]
    variables = line.split(",")
    if len(variables) < 0:
        greatbool = False

    return greatbool

def checkProcedure(line, greatbool):
    # Revisa si la definición de un Procedimiento es válida

    line = line[4:]
    procname = ""
    boolvalid = True
    if not "(" in line and not ")" in line:
        boolvalid = False

    if boolvalid:
        for letter in line:
            if letter != "(":
                procname += letter

    if len(procname) < 0 or not boolvalid or not line[-1:] == "{":
        greatbool = False

    return greatbool


if __name__ == '__main__':
    main()
