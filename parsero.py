"""
All the logic y regular expressions behind the parser
"""

import re


procedures = []

commandslist = ["walk", "jump", "drop", "grab", "get", "free", "pop"]
orientationList = ["north", "south", "east", "west"]
directionsList = ["around", "left", "right"]
walkList = orientationList.copy()
walkList.extend(["front", "back", "left", "right"])


commands = '|'.join(commandslist)
posibles_orientation = '|'.join(orientationList)
posibles_directions = '|'.join(directionsList)
posibles_walks = '|'.join(walkList)


start_prog = r'^[\s\n]*PROG[\s\n]*'
end_prog = r'GORP[\s\n]*$'

name_pattern = r'\w+[\w\d]*'
var_pattern = rf'^[\s\n]*VAR([\s\n]*{name_pattern}[\s\n]*,)*[\s\n]*{name_pattern}[\s\n]*;'

proc_pattern = rf'[\s\n]*PROC[\s\n]*({name_pattern})[\s\n]*\(([\s\n]*({name_pattern}[\s\n]*,[\s\n]*)*({name_pattern}))?[\s\n]*\)[\s\n]*'



def readFile(fileName):
    file = open(fileName, 'r')
    code = file.read()
    file.close()
    code = code.replace('{', '[')
    code = code.replace('}', ']')
    code = code.replace('\n', ' ')
    return code

def createBlockScope(parameters, variables, procedures, n_parameters , proc):
    posibles = variables.copy()
    callable_procedures = procedures.copy()
    # DEPRECATED CODE: NOT ALLOW RECURSIVE CALLS
    # try:
    #     callable_procedures.remove(proc)
    # except ValueError:
    #     pass
    posibles.extend(parameters)
    posibles_parameters = '|'.join(posibles)
    rules = []

    for k, v in n_parameters.items():
        for p in v:
            if p in callable_procedures:
                if k == 0:
                    exp = rf'[\s\n]*{p}[\s\n]*\([\s\n]*\)[\s\n]*'
                elif k == 1:
                    exp = rf'[\s\n]*{p}[\s\n]*\([\s\n]*({posibles_parameters}|\d+)[\s\n]*\)[\s\n]*'
                elif k > 1:
                    k_minus = k - 1
                    repeticiones = f'(({posibles_parameters}|\d+)\s*,\s*)'*k_minus
                    exp = rf'[\s\n]*{p}[\s\n]*\(\s*{repeticiones}\s*({posibles_parameters}|\d+)\s*\)[\s\n]*'
                rules.append(exp)

    posibles_procedures = '|'.join(rules)


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

    global_command_pattern = rf'({command_pattern}|{jumpTo_pattern}|{veer_pattern}|{look_pattern}|{walk_pattern}|{assign_pattern}|({posibles_procedures}))'

    terminal_block_pattern = rf'[\s\n]*({global_command_pattern}%)*({global_command_pattern})?[\s\n]*'

    if_pattern = rf'\s*if\s*\(({global_condition_pattern})\)\s*\[\s*{terminal_block_pattern}\s*\]\s*(else\s*\[{terminal_block_pattern}\])?\s*fi\s*'

    while_pattern = rf'\s*while\s*\(({global_condition_pattern})\)\s*do\s*\[\s*{terminal_block_pattern}\s*\]\s*od\s*'

    repeat_pattern = rf'\s*repeatTimes\s*(({posibles_parameters})|\d+)\s*\[\s*{terminal_block_pattern}\s*\]\s*per\s*'

    control_structure_pattern = rf'({if_pattern}|{while_pattern}|{repeat_pattern})'
    # print(terminal_block_pattern)

    return global_command_pattern, control_structure_pattern



def findVariables(code):
    variables = re.match(var_pattern, code)
    if variables:
        s = variables.span()[1]
        var_start = r'^[\s\n]*VAR'
        var_str = re.match(var_start, variables.group())
        just_variables = variables.group()[var_str.span()[1]:]
        variables = re.findall(name_pattern, just_variables)
        return code[s:], variables
    return False

def findProcedures(code):
    procedures = re.findall(proc_pattern, code)
    procedures = [p[0] for p in procedures]
    parameters = {}
    for p in procedures:
        proc = re.search(rf'[\s\n]*PROC[\n\s]*{p}', code)
        s = proc.span()
        temp_code = code[s[0]:]
        just_procedure = re.match(rf'^{proc_pattern}', temp_code)
        just_procedure = just_procedure.group()
        info = re.findall(name_pattern, just_procedure)
        parameters_act = info[2:]
        if len(parameters_act) in parameters:
            parameters[len(parameters_act)].append(p)
        else:
            parameters[len(parameters_act)] = [p]
    return procedures, parameters


def checkProgram(code):
    start = re.match(start_prog, code)
    end = re.search(end_prog, code)
    if start and end:
        s = start.span()[1]
        e = end.span()[0]
        return checkParenthesis(code[s:e])
    return False

def checkParenthesis(code):
    stack = []
    for char in code:
        if char in ['[', '(']:
            stack.append(char)
        elif char in [']', ')']:
            if not stack:
                return False
            current_char = stack.pop()
            if current_char == '[' and char != ']':
                return False
            elif current_char == '(' and char != ')':
                return False
    if stack:
        return False
    return code

def checkProcedure(code):
    procedure = re.match(rf'^{proc_pattern}', code)
    if procedure:
        s = procedure.span()[1]
        proc_start = r'^[\s\n]*PROC'
        proc_str = re.match(proc_start, procedure.group())
        just_procedure = procedure.group()[proc_str.span()[1]:]
        info = re.findall(name_pattern, just_procedure)
        procedure = info[0]
        parameters = info[1:]
        procedures.append(procedure)
        return code[s:], procedure, parameters
    return False

def checkNonTerminalBlock(code, command_pattern, control_structure_pattern):
    non_terminal_block_pattern = r'^\[[\s\n]*'
    non_terminal_block = re.match(non_terminal_block_pattern, code)
    if non_terminal_block:
        s = non_terminal_block.span()[1]
        code = code[s:]
        end = re.search(r'\][\s\n]*CORP', code)
        if end:
            e = end.span()[0]
        else:
            return False

        temp_block = code[:e]
        temp_block = re.sub(r'[\s\n]*', '', temp_block)
        inicios = []
        finales = []
        pos = -1
        while True:
            pos = temp_block.find('[', pos + 1)
            if pos == -1:
                break
            inicios.append(pos)

        while True:
            pos = temp_block.find(']', pos + 1)
            if pos == -1:
                break
            finales.append(pos)
        # print(inicios, finales)

        for i, j in zip(inicios, finales):
            temp_block = temp_block [:i] + temp_block[i:j].replace(';', '%') + temp_block[j:]
        # print(temp_block)

        instructions = temp_block.split(';')
        for ins in instructions:
            command = re.match(rf'{command_pattern}$', ins)
            if not command:
                control_structure = re.match(rf'{control_structure_pattern}$', ins)
                if not control_structure:
                    # print('Error: invalid instruction ' + ins)
                    return False
                # print('control structure ' + ins)
            else:
                pass
                # print('command ' + ins)

        end_pattern = r'^[\s\n]*\][\s\n]*CORP'
        end = re.match(end_pattern, code[e:])
        if end:
            return code[e+end.span()[1]:]

        return False

def checkInstructionsBlock(code, command_pattern, control_structure_pattern):
    start = r'^[\s\n]*\[[\s\n]*'
    end = r'[\s\n]*\][\s\n]*$'
    s = re.match(start, code)
    e = re.search(end, code)
    if s and e:
        s = s.span()[1]
        e = e.span()[0]
        code = code[s:e]
        # print(code)

        temp_block = re.sub(r'[\s\n]*', '', code)
        inicios = []
        finales = []
        pos = -1
        while True:
            pos = temp_block.find('[', pos + 1)
            if pos == -1:
                break
            inicios.append(pos)

        while True:
            pos = temp_block.find(']', pos + 1)
            if pos == -1:
                break
            finales.append(pos)
        # print(inicios, finales)

        for i, j in zip(inicios, finales):
            temp_block = temp_block [:i] + temp_block[i:j].replace(';', '%') + temp_block[j:]
        # print(temp_block)

        instructions = temp_block.split(';')
        for ins in instructions:
            command = re.match(rf'{command_pattern}$', ins)
            if not command:
                control_structure = re.match(rf'{control_structure_pattern}$', ins)
                if not control_structure:
                    # print('Error: invalid instruction ' + ins)
                    return False
                # print('control structure ' + ins)
            else:
                pass
                # print('command ' + ins)


        if len(code[e:]) <= 0:
            return True
        return False
