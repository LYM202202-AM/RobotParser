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

        # has_procedure = parser.checkProcedure(code)
        # if has_procedure:
        #     code, procedure, parameters = has_procedure
        #     block_pattern = parser.createBlockScope(parameters, variables, procedure)
        #     print(block_pattern)
    else:
        print("No program")


if __name__ == '__main__':
    main()