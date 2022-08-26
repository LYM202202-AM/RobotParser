import parsero

variables = []
procedures = []

def main(filename):
    """ Main function to execute the parser
    """
    try:
        code = parsero.readFile(filename)
    except FileNotFoundError:
        print("File not found")
        return False
    code = parsero.checkProgram(code)
    if code:
        has_variables = parsero.findVariables(code)
        if has_variables:
            code, variables = has_variables
            # print("Variables: ", variables)
        else:
            variables = []
            # print("No variables")

        has_procedures = parsero.findProcedures(code)
        if has_procedures:
            procedures, n_parameters = has_procedures
            # print("Procedures: ", procedures)
            # print("Number of parameters: ", n_parameters)
            # print()
            # procedures = has_procedures
            for proc_act in procedures:
                # # print("Procedure: ", proc_act)
                has_procedure = parsero.checkProcedure(code)
                if has_procedure:
                    code, proc, parameters = has_procedure
                    if proc == proc_act:
                        command_pattern, control_structure_pattern = parsero.createBlockScope(
                            parameters, variables, procedures, n_parameters, proc)
                        has_block = parsero.checkNonTerminalBlock(
                            code, command_pattern, control_structure_pattern)
                        if has_block:
                            code = has_block
                            # print('Procedure: ', proc)
                            # print('Parameters: ', parameters)
                            # # print('Variables: ', variables)
                            # # print(code)
                            # print('\n')
                        else:
                            # print('No valid procedure ' + proc)
                            return False
            instructions_block = parsero.createBlockScope(
                [], variables, procedures, n_parameters, [])
            # # print(code)
            command_pattern, control_structure_pattern = instructions_block

            final = parsero.checkInstructionsBlock(code, command_pattern, control_structure_pattern)


            if final:
                return True
                # print("Valid program")
            else:
                return False
                # print("Invalid program")

    else:
        return False
        # print("No program")


if __name__ == '__main__':
    tests_dir = 'tests/'
    filename = tests_dir + input("Enter the name of the file (must be in the folder tests/) to eval: ")
    if main(filename):
        print("Yes, the input file is a valid program.")
    else:
        print("No, the input file is not a valid program.")
