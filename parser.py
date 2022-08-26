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
var_pattern = rf'^[\s\n]*VAR([\s\n]*{name_pattern},)*[\s\n]*{name_pattern};'

proc_pattern = rf'[\s\n]*PROC[\s\n]*({name_pattern})[\s\n]*\('
# proc_pattern = rf'[\s\n]*PROC[\s\n]*(\w+[\w\d]*)[\s\n]*\((2(3[\s\n]*(1[\w\d]*,[\s\n]*1)*(\w+[\w\d]*)3)?[\s\n]*\)2)'

def readFile(fileName):
    file = open(fileName, 'r')
    code = file.read()
    file.close()
    return code

def checkProgram(code):
    start = re.match(start_prog, code)
    end = re.search(end_prog, code)
    if start and end:
        s = start.span()[1]
        e = end.span()[0]
        return code[s:e]
    return False

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
    pass

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



def createBlockScope(parameters, variables, procedure):
    posibles = variables.copy()
    callable_procedures = procedures.copy()
    callable_procedures.remove(procedure)
    posibles.extend(parameters)
    posibles.extend(callable_procedures)
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

    terminal_block_pattern = rf'[\s\n]*((({global_command_pattern})([\s\n]*;[\s\n]*))*{global_command_pattern})?[\s\n]*'

    if_pattern = rf'^\s*if\s*\(({global_condition_pattern})\)\s*\[\s*{terminal_block_pattern}\s*\]\s*(else\s*\[{terminal_block_pattern}\])?\s*fi\s*'

    while_pattern = rf'^\s*while\s*\(({global_condition_pattern})\)\s*do\s*\[\s*{terminal_block_pattern}\s*\]\s*od\s*'

    repeat_pattern = rf'^\s*repeatTimes\s*(({posibles_parameters})|\d+)\s*\[\s*{terminal_block_pattern}\s*\]\s*per\s*'

    control_structure_pattern = rf'({if_pattern}|{while_pattern}|{repeat_pattern})'

    non_terminal_block_pattern = rf'[\s\n]*((({global_command_pattern}|{control_structure_pattern})([\s\n]*;[\s\n]*))*({global_command_pattern}|{control_structure_pattern}))?[\s\n]*'

    return non_terminal_block_pattern