import sys

"""
File <- str
Intended to store the file's name

Instruction <- array of str
Intended to store an instruction in the form of array of strings
Instructions are either:
    -A-instructions, in the form of ["@", decimalNumber]
    -C-instructions, in the form of [DEST, COND, JUMP].

Program <- array of Instructions
Intended to store multiple instructions making up the whole program

TextProgram <- array of str
Intended to store multiple instructions written as strings

SymbolTable <- dict
Intended to store all the names of the symbols and their respective value

LabelName <- str
The name of the label
"""

# File -> TextProgram
def preAssemble(fileName):
    """
    This function loads the file, removes all the whitespace
    and returns an array of the single instruction written
    as strings
    """
    try:
        imported = open(fileName, 'r')
    except:
        print("Something went wrong with file-reading")
        sys.exit(0)
    textProgram = []
    for line in imported:
        flag = False
        temp = ""
        for character in line:
            if (character == " " or character == "\n"):
                pass
            elif (character == "/"):
                if (flag):
                    temp = temp[:-1]
                    break
                flag = True
                temp += character
            else:
                temp += character
        if (temp):
            textProgram.append(temp)
    imported.close()
    return textProgram

# TextProgram -> Program, SymbolTable
def textToProgram(textProgram):
    """
    This function takes a TextProgram as input and returns
    a Program with its SymbolTable
    """
    program = []
    symbolTable = {}

    for textInstruction in textProgram:
        instruction, labelName = textToInstruction(textInstruction)
        if (labelName):
            symbolTable[labelName] = len(program)
        else:
            program.append(instruction)
    
    return program, symbolTable

# TextInstruction -> Instruction, LabelName
# textToProgram's helper function
def textToInstruction(textInstruction):
    """
    This function takes a TextInstruction as input and returns
    an Instruction with its SymbolTable
    """

    if (textInstruction[0] == "("):
        """
        This is a label declaration
        """
        return ["",], textInstruction[1:-1]

    elif (textInstruction[0] == "@"):
        """
        This is an A instruction.
        """
        return ["@", textInstruction[1:]], ""

    else:
        """
        This is a C instruction, we have to find:
            -a DEST
            -a COND
            -a JUMP
        """
        dest = ""
        cond = ""
        jump = ""

        # looking for DEST, COND and JUMP
        temp = ""
        for character in textInstruction:
            if (character == "="):
                dest = temp
                temp = ""

            elif (character == ";"):
                cond = temp
                temp = ""
            else:
                temp += character
        if (cond):
            jump = temp
        else:
            cond = temp
        return [dest, cond, jump], ""
    
# Program, SymbolTable -> Program, SymbolTable
def desymbolize(program, symbolTable):
    """
    Removes all symbols, including default labels and variables,
    and returns the cleaned Program and updated SymbolTable
    """
    newProgram = []
    for instruction in program:
        if (instruction[0] == "@"):
            """
            A-instruction, need to convert from string to number the second element
            """
            try:
                """
                Check if it is a number
                """
                instruction[1] = int(instruction[1])
            except ValueError:
                """
                Check if it is a default label
                """
                if (instruction[1] == "SP"):
                    instruction[1] = 0
                elif (instruction[1] == "LCL"):
                    instruction[1] = 1
                elif (instruction[1] == "ARG"):
                    instruction[1] = 2
                elif (instruction[1] == "THIS"):
                    instruction[1] = 3
                elif (instruction[1] == "THAT"):
                    instruction[1] = 4
                elif (instruction[1] in ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"]):
                    instruction[1] = int(instruction[1][1:])
                elif (instruction[1] == "SCREEN"):
                    instruction[1] = 16384
                elif (instruction[1] == "KBD"):
                    instruction[1] = 24576
                elif (instruction[1] in symbolTable):
                    instruction[1] = symbolTable[instruction[1]]
                else:
                    symbolTable[instruction[1]] = len(symbolTable) + 16
                    instruction[1] = symbolTable[instruction[1]]
            newProgram.append(["@", instruction[1]])
        else:
            """
            This is a C-instruction, just return it
            """
            newProgram.append(instruction)
    return newProgram

def assemble(program, symbolTable, fileName):
    try:
        file = open(fileName + ".hack", "w")
    except:
        print("Something went wrong with file-writing")
        sys.exit(0)

    for instruction in program:
        if (instruction[0] == "@"):
            """
            A-instruction
            """
            binaryInstruction = bin(instruction[1])[2:]
            binaryInstruction = "0" * (16-len(binaryInstruction)) + binaryInstruction
            file.write(binaryInstruction + "\n")
        else:
            """
            C-instruction
            """
            binaryInstruction = "111" + compEvaluation(instruction[1]) + destEvaluation(instruction[0]) + jumpEvaluation(instruction[2])
            file.write(binaryInstruction + "\n")
    file.close()

# Part of Instruction -> BinaryInstruction        
def compEvaluation(comp):
    if (comp == "0"):
        return "0101010"
    elif (comp == "1"):
        return "0111111"
    elif (comp == "-1"):
        return "0111010"
    elif (comp == "D"):
        return "0001100"
    elif (comp == "A"):
        return "0110000"
    elif (comp == "!D"):
        return "0001101"
    elif (comp == "!A"):
        return "0110001"
    elif (comp == "-D"):
        return "0001111"
    elif (comp == "-A"):
        return "0110011"
    elif (comp == "D+1"):
        return "0011111"
    elif (comp == "A+1"):
        return "0110111"
    elif (comp == "D-1"):
        return "0001110"
    elif (comp == "A-1"):
        return "0110010"
    elif (comp == "D+A"):
        return "0000010"
    elif (comp == "D-A"):
        return "0010011"
    elif (comp == "A-D"):
        return "0000111"
    elif (comp == "D&A"):
        return "0000000"
    elif (comp == "D|A"):
        return "0010101"
    elif (comp == "M"):
        return "1110000"
    elif (comp == "!M"):
        return "1110001"
    elif (comp == "-M"):
        return "1110011"
    elif (comp == "M+1"):
        return "1110111"
    elif (comp == "M-1"):
        return "1110010"
    elif (comp == "D+M"):
        return "1000010"
    elif (comp == "D-M"):
        return "1010011"
    elif (comp == "M-D"):
        return "1000111"
    elif (comp == "D&M"):
        return "1000000"
    elif (comp == "D|M"):
        return "1010101"
    else:
        print("C-instruction management went wrong")

# Part of Instruction -> BinaryInstruction        
def destEvaluation(dest):
    binaryInstruction = ""
    if ("A" in dest):
        binaryInstruction += "1"
    else:
        binaryInstruction += "0"
    if ("D" in dest):
        binaryInstruction += "1"
    else:
        binaryInstruction += "0"
    if ("M" in dest):
        binaryInstruction += "1"
    else:
        binaryInstruction += "0"
    return binaryInstruction

# Part of Instruction -> BinaryInstruction        
def jumpEvaluation(jump):
    if (jump == ""):
        return "000"
    elif (jump == "JGT"):
        return "001"
    elif (jump == "JEQ"):
        return "010"
    elif (jump == "JGE"):
        return "011"
    elif (jump == "JLT"):
        return "100"
    elif (jump == "JNE"):
        return "101"
    elif (jump == "JLE"):
        return "110"
    elif (jump == "JMP"):
        return "111"

def wrapper(fileName):
    textProgram = preAssemble(fileName + ".asm")
    program, symbolTable = textToProgram(textProgram)
    program = desymbolize(program, symbolTable)
    assemble(program, symbolTable, fileName)

print("Input the name of the file, without extension, that you want to convert")
print("The file must be in the same folder as this program")
wrapper(input("(Case sensitive) "))