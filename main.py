import parsero

variables = []
procedures = []

def main():
    """ Main function to execute the parser
    """
    code = parsero.readFile("tests/test.txt")
    code = parsero.checkProgram(code)
    if code:
        has_variables = parsero.findVariables(code)
        if has_variables:
            code, variables = has_variables
            print("Variables: ", variables)
        else:
            variables = []
            print("No variables")

        has_procedures = parsero.findProcedures(code)
        if has_procedures:
            procedures, n_parameters = has_procedures
            print("Procedures: ", procedures)
            print("Number of parameters: ", n_parameters)
            print()
            # procedures = has_procedures
            for proc_act in procedures:
                # print("Procedure: ", proc_act)
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
                            print('Procedure: ', proc)
                            print('Parameters: ', parameters)
                            # print('Variables: ', variables)
                            # print(code)
                            print('\n')
                        else:
                            print('No valid procedure ' + proc)
            instructions_block = parsero.createBlockScope(
                [], variables, procedures, n_parameters, [])
            # print(code)
            command_pattern, control_structure_pattern = instructions_block

            final = parsero.checkInstructionsBlock(code, command_pattern, control_structure_pattern)


            if final:
                print("Valid program")
            else:
                print("Invalid program")

    else:
        print("No program")


if __name__ == '__main__':
    main()
