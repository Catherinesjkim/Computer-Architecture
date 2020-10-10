"""
TK Video 1: CPU Stack

1. What happens if you PUSH too many items on the stack? Stack overflow occurs

2. What happens if you POP from an empty stack? Stack underflow occurs

3. How can you detect if the stack is empty? Check the address 0XFF? Then it's empty

4. What information must be saved on the stack when the CPU is servicing an interrupt? Why?


TK Video 2: CPU Interrups

1. If there were no interrupts, how would the CPU have to detect keyboard input?

2. Why are interrupts better?

3. What other kinds of devices might cause interrupts to be issued?

"""

"""
Mari's Lecture: 

CPU Stack

Used by the CPU to save state and store data

Stack Pointer (SP): a register (R7) that stores the address of the topmost element of the stack

Two main operations:
 
1. push - decrease the stack pointer and write the element at the top of the stack

2. pop - read the element from the top of the stack and increase the stack pointer


Stack Overflow: Stack keeps growing down --> stack overflow happens when it keeps growing

Stack Underflow: What happens when you pop an empty stack? "You can't pop an empty stack"

C doesn't let you know there's a stack overflow and let's you keep getting added to the stack.
Python let's you know and says can't keep getting added to the stack. 

How computers save state and how recursive function under the hood (uses stack)

We need to use stack to do subroutines == functions

"""

PRINT_HI = 1  # prints hi
HALT = 2  # HLT
PRINT_NUM = 3
SAVE = 4  # save a value to a register (LDI)
# prints the value of a register (hardware - faster than memory/RAM)
PRINT_REGISTER = 5
ADD = 6  # adds values from two registers x, y and stores it in register x
PUSH = 7
POP = 8

# pc: contains the location of the instruction being executed in the RAM
pc = 0  # program counter - points to the instruction we're currently executing
running = True

# this is how recursie and complicated function calls are implemented
def loadMemory():
    # in guided project, it will be in binary format
    # our program, a set of instructions
    # memory = RAM (registers, random access memory (RAM) - temporary)
    memory = [
        PRINT_HI,  # prints hi
        SAVE, # saves 65 into register 2
        65,
        2, # halt
        PUSH, # push value (65) in reg 2 to the stack
        2,  # halt
        SAVE, # saves 99 into register 2
        99,
        2,  # halt
        PUSH, # push value (99) in reg 2 to the stack
        2,  # halt
        POP, # pop value (99) and store it in reg 0
        0,
        PRINT_REGISTER, # print value stored in reigster 0 (99)
        0, 
        POP, # pop value (65) and store it in reg 0
        0,
        PRINT_REGISTER, # print value stored in register 0 (65)
        0,
        HALT # stop the program
    ]
    spaceForStack = 128 - len(memory) # assume we have 128 bytes of memory only
    memory += [0] * spaceForStack
    return memory
    
memory = loadMemory()
pc = 0 # program counter - points to the instruction we're currently executing
print(memory)
SP = 7
registers = [0] * 8
registers[SP] = len(memory) - 1 # 127
    
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
        
    elif commandToExecute == PUSH: 
        # takes in a register number and saves the value in it
        # decrement the stack pointer
        # SP = 7
        registers[SP] -= 1 # decrement by 1
        # store the value in the register onto the top of the stack
        registerToGetValueIn = memory[pc + 1] # pc + 1 = 3
        # 
        valueInRegister = registers[registerToGetValueIn]
        # do this on top of the stack
        memory[registers[SP]] = valueInRegister  # [registers[SP]] is always pointing to the top of the stack
        # increment the program counter to go to the next instruction to execute
        pc += 2
    
    # exact opposite of push
    elif commandToExecute == POP:
        # pops the value from the top of the stack and stores it in a given register
        # read the value from the top of the stack
        topmostValueInStack = memory[registers[SP]] # will always give you the address of the top of the stack, index in the memory
        # store value to the given register
        registerToStoreItIn = memory[pc + 1]
        registers[registerToStoreItIn] = topmostValueInStack
        # increment stack pointer
        registers[SP] += 1
        # increment the program counter to go to the next instruction to execute
        pc += 2
    
    else:
        print("ehh idk what to do")
        sys.exit(1)
