import sys

# 0b - binary numeration in python
# Operation Codes - Opcodes - asssigning constant variable for easier understanding
PRINT_HELLO_WORLD = 1  # 0b00000001
HALT              = 2  # 0b00000010  - Halt the CPU (and exit the emulator)
PRINT_NUM         = 3  # 0b00000011
SAVE_REG          = 4  # 0b00000110 - will take the value and register
PRINT_REG         = 5  # 0b00000111
ADD               = 6  # 0b00001110
PUSH              = 7  # 0b00001111
POP               = 8  # 0b00011110
CALL              = 9  # 0b00011111 - Call location in memory where a coroutine starts 1. Move PC to location given by register; 2. Store the return address in the Stack
RET               = 10 # 0b00111110 - Return from subroutine - move pc to where it came from - pop from stack, set PC to the value

# ADD takes TWO reigsters, adds their values
# and stores the result in the first register given

# program that adds two numbers together
# return

# persistent storage - can store a lot of data
memory = [0] * 256

# 8 registers - very few storage - preferred to do for super-fast access
registers = [0] * 8

# Stack Pointer: the register that saves the current value - what is the address location? 255 --> 254 --> 253...
SP = 7

running = True

# Program Counter
pc = 0

# Get file name from command line arguments - we have a couple of guards up
if len(sys.argv) != 2:
    print("Usage: You forgot to add the filename print_nums.ec after artem_cpu.py")
    sys.exit(1) # operating system - exited in a bad way, it failed to do sth. Similar to 500 for a server
    
# Open a file and load into memory - traverse a file
def load_memory(filename):
    address = 0
    try: 
        with open(filename) as file: # open a file and
            # read line by line
            for line in file:
                # Split the current line on the start of the comment '#' symbol
                split_line = line.split('#')
                # print(split_line)
                
                code_value = split_line[0].strip() # this removes/strips whitespace and \n character

                # got rid of the line gaps \n by adding int --> converted the whole line into an integer
                # Make sure that the value before the # symbol is not empty
                if code_value == '':
                    continue
                
                # turn any binary code into a number/integer
                num = int(code_value)
                # to store into a memory
                memory[address] = num
                # moving the array pointer over
                address += 1
                
                                     
    except FileNotFoundError:
        print(f"{sys.argv[1]} --> *** File Not Found ***")
        sys.exit(2) # any number besides 0, it means failed: 2 == FileNotFoundError
    
    
load_memory(sys.argv[1])

while running:
    # Read line by line from Memory
    instruction = memory[pc]
    
    if instruction == PRINT_HELLO_WORLD:
        # print Hello world
        # move the PC up 1 to the next instruction
        print("Hello World")
        pc += 1
        
    elif instruction == PRINT_NUM:
        # Print the number in the NEXT memory slot
        num = memory[pc + 1]
        print(num)
        pc += 2
    
    # Same as LDI
    elif instruction == SAVE_REG:
        # Save some value to some register
        # First number after instruction will be the Value to store
        # Second number after instruction will be register
        num = memory[pc + 1]
        reg_location = memory[pc + 2]
        registers[reg_location] = num
        pc += 3
        
    elif instruction == PRINT_REG:
        reg_location = memory[pc + 1]
        print(registers[reg_location])
        pc += 2
        
    elif instruction == ADD:
        # ADD takes TWO registers, adds their values
        # and stores the result in the first register given 
        # Get register 1
        # get register 2
        # Add the values of both registers together
        # Store in register 1
        reg_1 = memory[pc + 1]
        reg_2 = memory[pc + 2]
        registers[reg_1] += registers[reg_2]
        pc += 3
        
    elif instruction == HALT:
        running = False
        pc += 1
        print(memory[-20:])
        print(registers)
    
    # address = location in memory - context of memory
    elif instruction == PUSH:
        # pointer = variable that points an address
        given_register = memory[pc + 1]
        value_in_register = registers[given_register]
        # decrement the Stack Pointer
        registers[SP] -= 1
        # write the value of the given register to memory at the SP location
        memory[registers[SP]] = value_in_register
        pc += 2
    
    # retrieve a number/value --> back to the register
    elif instruction == POP:
        given_register = memory[pc + 1]
        # Write the value in memory at the top of stack to the given register
        value_from_memory = memory[registers[SP]]
        registers[given_register] = value_from_memory
        # increment the Stack Pointer
        registers[SP] += 1
        pc += 2
        
    elif instruction == CALL:
        # Get the given register in the operand
        given_register = memory[pc + 1]
        # Store the return address (PC + 2) onto the stack
        # decrement the Stack Pointer
        registers[SP] -= 1
        # write the return address
        memory[registers[SP]] = pc + 2
        # SET PC to the value inside given_register
        pc = registers[given_register]
        # we should not move the program counter anymore automatically because we directly manipulated it.
    
    # Once we are done running with a coroutine, we want to come back where we came from
    # Pop from the stack, and simply set the pc from the value that was popped
    elif instruction == RET:
        # set PC to the value at the top of the stack
        pc = memory[registers[SP]]
        # POP from stack: set the registers, plus equals to 1 (we want to move back up)
        registers[SP] += 1 
    else:
        print(f"Unknown instruction {instruction}")
        sys.exit(1)
