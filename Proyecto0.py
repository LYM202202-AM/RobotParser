
def main():
    code = open("C:\\Users\\manue\\Documents\\Uniandes\\2022-2\\LYM\\Prueba.txt", "r")
    code = code.read()
    if (code[:4]) == "PROG" and (code[-4:]) == "GORP":
        code = code[4:]
        code = code[:-4]
        whitelist = set('abcdefghijklmnopqrstuvwxyz{[()]}/-,;ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        code = ''.join(filter(whitelist.__contains__, code))
        code = code.replace("{", "{;")
        code = code.replace("}", "};")
        code = code.split(";")
        print(code)

        greatbool = True
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
                #     line[counter:]

    print(greatbool)
    return greatbool

def checkVariables(line, greatbool):
    "Revisa las declaraciones de variables"
    line = line[3:]
    variables = line.split(",")
    if len(variables) < 0:
        greatbool = False

    return greatbool

def checkProcedure(line, greatbool):
    "Revisa si la definición de un Procedimiento es válida"

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


main()
