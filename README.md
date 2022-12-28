# Robot Parser
Welcome to the Robot Parser repository! This Python program is designed to parse a text file containing a program for a robot, and verify that the syntax is correct.

## Features
- Reads a text file containing a program for the robot
- Verifies that function names and variable names have been previously defined or, in the case of functions, that they are the function's arguments
- Allows recursion
- Ignores spaces and tabulators (except within instructions)

## How to Use

To use the Robot Parser, follow these steps:

- Clone this repository to your local machine using `git clone https://github.com/LYM202202/robot-parser.git`
- Navigate to the repository directory using `cd robot-parser`
- Run the parser by executing `python main.py`
- The program will prompt you to enter the name of a file located in the tests directory. You can enter the name of one of the test files provided (e.g. test.txt), or the name of a file you have created yourself.

## Authors

- Abel Arismendy (a.arismendy@uniandes.edu.co)
- Manuela Pacheco (m.pachecom2@uniandes.edu.co)

## Tests

The folder [tests](/tests/) contains 3 files:

- [test.txt](/tests/test.txt) is a valid program without recursive calls.
- [test1.txt](/tests/test1.txt)is a valid program with recursive calls.
- [test2.txt](/tests/test2.txt) is a not valid program.

More info in the [document](/docs/L&M-202220-Project0.pdf)
