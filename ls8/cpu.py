"""
The CPU consists of 2 parts:
1. Arithmetic/Logic Unit (ALU): the circuitry that performs data manipulation
2. Control Unit: the circuitry for coordinating machine activities

A register is a slot for storing a single value on the CPU similar to main memory cells. Registers are like the "workbench" of the CPU. For the CPU to work with a piece of data, it has to be in one of the registers. However, since there are just a few registers, only a minimal amount of data can be loaded at any given time. Programs work around this by loading values from memory into registers, calculating values into other registers, and then storing the final results back in memory. They serve as temporary holding areas for data being manipulated by the CPU such as input/output to the ALU. 

The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total. It has 10 total registers, each of which is 16 bits. Most of them are general purpose, but a few have designated roles.

8 general purpose registers (R0-R7): can be used to perform any program calculations. 
1 program counter (pc) special registers: an unsigned integer which is the address of the next instruction in memory to execute
1 condition flags (COND) speical register: tell us info about the previous calculation

To perform operations on data stored in main memory, it is the responsibility of the control unit to:
    - Transfer the data into the registers
    - Inform the ALU which registers hold the pertinent data to operate on
    - Inform the ALU what register should receive the result
    
Registers hold data that should be immediately accessible, whereas main memory is for data that is less likely to be needed in the near future

In many modern computers, an additional level of storage called cache memory which can be used to temporarily store data from main memory that can be used by the CPU, offering the ability to make less round trips when receiving and storing data before finally committing to main memory if needed

Bus
- To transfer data between the CPU and main memory, data is transferred by a collection of wires called a bus
- Through this bus the CPU is able to read memory via its address and similarly write to memory in the same manner

Instructing the machine

The CPU performs its operations in sequence which is collectively called a program. These operations are defined by a series of machine instructions that fall into 3 categories:

1. Data transfer: operations to transfer/copy data from one location to another

2. Arithmetic/Logic: Instructions to manipulate data within the ALU, such as logical operations such as AND, OR, XOR, and NOT and traditional addition and subtraction

3. Control/Instruction Set
    - Instructions that, according to "direct the execution of the program rather than the manipulation of data"
    - This includes conditional operations that support branching e.g. CMP (compare) and JUMP
    
Flags

- The flags register FL and holds the current flags status. These flags can change based on the operands given to the CMP opcode

FL bits: 00000LGE
- L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise
- G Greater-than: during a CMP, set to 1
- E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise


"""

"""CPU functionality."""

import sys

"""
Instruction Set: an instruction is a command which tesll the CPU to do some fundamental task, such as add 2 numbers. Instructions have both an opcode which indicates the kind of task to perform and a set of parameters which provide inputs to the task being performed

Each opcode represents one task that the CPU "knows" how to do. There are just 16 opcodes in LS-8. Everything the computer can calculate is some sequence of these simple instructions. Each instruction is 16 bits long, with the left 4 bits storing the opcode. The rest of the bits are used to store the parameters
"""
ADD = 0b10100000 # It takes 2 numbers, adds them together, and stores the result in registerA (pop 2 operands, add, push result) handled by the ALU.
AND = 0b10101000 # Instruction handled by the ALU. Bitwise-AND the values in registerA and registerB, then store the result in registerA
LDI = 0b10000010 # LDI register immediate. Load InDirect/immediate. Set the value of a register to an integer. It's used to load a value from a location in memory into a register
PRN = 0b01000111 # PRN register. Pseudo-instruction that pritns numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register
HLT = 0b00000001 # Halt the CPU (and exit the emulator)
INC = 0b01100101 # INC register. Instructin handled by ALU. Increment (add 1 to) the value in the given register
MUL = 0b10100010 # Instruction handled by ALU. Multiply the values in two registers together and store the result in registerA. 
PUSH = 0b01000101 # PUSH register. Push the value in the given register on the stack. 
POP = 0b01000110 # POP register. Pop the value at the top of the stack into the given register. Toss out the top of stack
CALL = 0b01010000 # CALL register - calls a subroutine (function) at the address stored in the register
RET = 0b00010001 # RET. Return from subroutine. Pop the value from the top of the stack and store it in the PC. It's listed as a separate instruction in the spec, since it's different keyword in assembly. It's a speical case of JMP. RET happens whenever R1 is 7. Return from function, expected result on top of stack
CMP = 0b10100111 # Compare is the same as subtraction except that the result value is not stored - handled by ALU
DEC = 0b01100110 # DEC register: Instruciton handled by the ALU. Decrement (subtract 1 from) the value in the given register
DIV = 0b10100011 # Instruction handled by the ALU. Divide the value in the first register by the value in the second, storing the result in registerA. If the value in the second register is 0, the system should print an error message and halt
JMP = 0b01010100 # Jump register. Jump to the address stored in the given register. Set the PC to the address stored in the given register. 
JEQ = 0b01010101 # JEQ register. If equal flag is set (true), jump to the address stored in the given register
JNE = 0b01010110 # JNE register. If E flag is clear (false, 0), jump to the address stored in the given register. Jump if Condition is Met - conditional jump that follows a test - it's commonly found after a CMP instruction

# R7 is reserved as the Stack Pointer (SP). SP points at the value at the top of the stack (most recently pushed), or address F4 if the stack is empty
sp = 7

# Centeral Processing Unit
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Step 1: Construct a new CPU."""
        # initialize the ram with 256 bytes
        self.ram = [0] * 256  # self.ram is a list of 256 zeroes
        # initialize 8 registers
        self.reg = [0] * 8 # just like the memory, we will store the reigsters in an array
        # internal registers
        self.pc = 0  # pc is an unsigned integer which is the address of the next instruction in memory to execute
        self.reg[sp] = 0xF4
        # FL == Flags
        self.FL = None
    
    # Step 2: Add RAM functions
    # add method ram_read() that accesses the RAM inside the CPU object
    # it should accept the address to read and return the value stored there
    def ram_read(self, register_address):
        return self.ram[register_address]
    
    # add method ram_write() that accesses the RAM inside the CPU object
    # ram_write() should accept a value to write, and the address to write it to.
    def ram_write(self, register_address, value_to_write):
        self.ram[register_address] = value_to_write
        return self.ram_read(register_address)
        

    # Step 7: Un-hardcode the machine code
    # LDI: load "immediate", store a value in a register, or "set this register to this value"
    # To move the contents of one memory cell to another,
    # First the machine must LOAD the memory from memory location #1 and store it in register A
    # Second instruction should then STORE the contents of register A in memory location #2
    # LOAD memory location 1 into register A
    # STORE contents of register A in memory location # 2
    def load(self):
        """Load a program into memory."""
        
        address = 0

        # print8.ls8: Print the number 8 on the screen
        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
            

    # ALU: Arithmetic/Logic Unit - the first part of CPU - the circuitry that performs data manipulation
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    # Step 3: Implement the core of CPU's run() method
    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            # self.trace()
            inst_register = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            # Step 5: Add the LDI instruction
            if inst_register == LDI:
                # print(f'operand 1:{operand_a} \n operand 2: {operand_b}, res hex (8): {0b00001000}')
                # reg num is going to have operand:a
                # value is number where we can have the number
                self.reg[operand_a] = operand_b
                self.pc += 3
            # Step 6: Add the PRN instruction
            # At this point, I should be able to run the program and have it print 8 to the console!
            elif inst_register == PRN:
                value_to_print = self.reg[operand_a]
                print(f'PRN --> {value_to_print}')
                self.pc += 2
            
            # Step 4: Implement the HLT instruction handler
            # halt stops the execution of the prgram
            elif inst_register == HLT:
                self.running = False
            else:
                sys.exit(1)
            
    

