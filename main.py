import re
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
        else:
            print("No variables")

        has_procedures = parser.findProcedures(code)
        if has_procedures:
            print("Procedures: ", has_procedures)
            procedures = has_procedures
            for proc_act in procedures:
                has_procedure = parser.checkProcedure(code)
                if has_procedure:
                    code, proc, parameters = has_procedure
                    if proc == proc_act:
                        command_pattern, control_structure_pattern = parser.createBlockScope(parameters, variables, procedures, proc)
                        has_block = parser.checkNonTerminalBlock(code, command_pattern, control_structure_pattern)
                        if has_block:
                            code = has_block
                            print('Procedure: ', proc)
                            print('Parameters: ', parameters)
                            print('Variables: ', variables)
                        else:
                            print('No valid procedure ' + proc)
    else:
        print("No program")


if __name__ == '__main__':
    main()