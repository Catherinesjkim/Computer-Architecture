# similar to the guided project
import sys

# a simple data-driven  machine that reads instructions out of Memory and executes them
# convention: constants are written in capital letter
# PRINT_HI & HALT: number representation of instructions
# instruction/opcode: this number means "to do this instruction"
PRINT_HI = 1 # PRN
HALT = 2 # HLT
PRINT_NUM = 3
SAVE = 4 # save a value to a register (LDI)
PRINT_REGISTER = 5 # prints the value of a register (hardware - faster than memory/RAM)
ADD = 6 # adds values from two registers x, y and stores it in register x

# pc: contains the location of the instruction being executed in the RAM
pc = 0 # program counter - points to the instruction we're currently executing
running = True

# in guided project, it will be in binary format
# our program, a set of instructions
# memory = RAM (registers, random access memory (RAM) - temporary)
memory = [
    PRINT_HI, # prints hi
    SAVE, # saves 65 into register 2
    65, 
    2,
    SAVE, # saves 20 into register 3
    20, # the value that we want to give
    3, # register number
    ADD, # take values in reg2 (65) and reg3 (20) and store the sum in reg2 (85)
    2, 
    3,
    PRINT_REGISTER, # print 85
    2,
    HALT # stop the program
]

# register in an array with 8 registers (we assume that there are 8 registers)
registers = [0] * 8

while running:
    commandToExecute = memory[pc]
    
    if commandToExecute == PRINT_HI:
        print("hi")
        # go to the next instruction we want to execute
        pc += 1
    elif commandToExecute == HALT:
        running = False
    elif commandToExecute == PRINT_NUM:
        numToPrint = memory[pc + 1]
        print(numToPrint)
        # passing in an operand == 2
        pc += 2
    elif commandToExecute == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(registers[reg]) 
        # passing in an operand == 2
        pc += 2
    elif commandToExecute == SAVE:
        numToSave = memory[pc + 1]
        registerToSaveItIn = memory[pc + 2]
        registers[registerToSaveItIn] = numToSave
        pc += 3
    elif commandToExecute == ADD:
        regA = memory[pc + 1]
        regB = memory[pc + 2]
        sumOfRegisters = registers[regA] + registers[regB]
        # overwriting the value at the first register with that sum
        registers[regA] = sumOfRegisters
        # increment the program counter by 3
        pc += 3
    else:
        print("ehh idk what to do")
        sys.exit(1)

    
