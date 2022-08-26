import parser

variables = []
procedures = []

def main():
    code = parser.readFile("tests/test.txt")
    code = parser.checkProgram(code)
    if code:
        has_variables = parser.findVariables(code)
        if has_variables:
            code, variables = has_variables
            print("Variables: ", variables)
        else:
            variables = []
            print("No variables")

        has_procedures = parser.findProcedures(code)
        if has_procedures:
            procedures, n_parameters = has_procedures
            print("Procedures: ", procedures)
            print("Number of parameters: ", n_parameters)
            print()
            # procedures = has_procedures
            for proc_act in procedures:
                # print("Procedure: ", proc_act)
                has_procedure = parser.checkProcedure(code)
                if has_procedure:
                    code, proc, parameters = has_procedure
                    if proc == proc_act:
                        command_pattern, control_structure_pattern = parser.createBlockScope(parameters, variables, procedures, n_parameters, proc)
                        has_block = parser.checkNonTerminalBlock(code, command_pattern, control_structure_pattern)
                        if has_block:
                            code = has_block
                            print('Procedure: ', proc)
                            print('Parameters: ', parameters)
                            # print('Variables: ', variables)
                            # print(code)
                            print('\n')
                        else:
                            print('No valid procedure ' + proc)
            instructions_block = parser.createBlockScope([], variables, procedures, n_parameters, [])
            # print(code)
            command_pattern, control_structure_pattern = instructions_block

            final = parser.checkInstructionsBlock(code, command_pattern, control_structure_pattern)


            if final:
                print("Valid program")
            else:
                print("Invalid program")

    else:
        print("No program")


if __name__ == '__main__':
    main()