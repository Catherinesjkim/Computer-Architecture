"""CPU functionality."""

import sys

ADD = 0b10100000
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

sp = 7

# Centeral Processing Unit
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Step 1: Construct a new CPU."""
        self.ram = [0] * 256  # self.ram is a list of 256 zeroes
        self.reg = [0] * 8
        self.pc = 0
        self.reg[sp] = 0xF4
        self.FL = 0b00000000
    
    # Step 2: Add RAM functions
    # add method ram_read() that accesses the RAM inside the CPU object
    # it should accept the address to read and return the value stored there
    def ram_read(self, ram_address):
        ram_value = self.ram[ram_address]
        return ram_value
    
    # add method ram_write() that accesses the RAM inside the CPU object
    # ram_write() should accept a value to write, and the address to write it to.
    def ram_write(self, ram_value, ram_address):
        self.ram[ram_address] = ram_value
        
    # LDI: load "immediate", store a value in a register, or "set this register to this value"
    # Step 7: Un-hardcode the machine code
    def load(self):
        """Load a program into memory."""

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
            

    # ALU: Arithmetic/Logic Unit
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        runnning = True
        
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
        
        # Step 5: Add the LDI instruction
        if ir == LDI:
            self.reg[operand_a] = operand_b
        
        # Step 6: Add the PRN instruction
        elif ir == PRN:
            print_item = self.ram[self.pc + 1]
            print(self.reg[print_item])
            
        # Step 4: Implement the HLT instruction handler
        elif ir == HLT:
            running = False
            
        elif ir == ADD:
            self.alu(ir, operand_a, operand_b)
            
        elif ir == MUL:
            self.alu(ir, operand_a, operand_b)
            
        elif ir == CMP:
            self.alu(ir, operand_a, operand_b)
            
        elif ir == PUSH:
            self.reg[sp] -= 1
            self.ram[self.reg[sp]] = self.reg[operand_a]
            
        elif ir == POP:
            self.reg[operand_a] = self.ram[self.reg[sp]]
            self.reg[sp] += 1
            
        elif ir == CALL:
            self.reg[sp] -= 1
            jump_point = self.pc + (ir >> 6) + 1
            self.ram[self.reg[sp]] = jump_point
            self.pc = self.reg[operand_a]
            continue
        
        elif ir == RET:
            ret_value = self.ram[self.reg[sp]]
            self.pc = ret_value
            self.reg[sp] += 1
            continue
        
        elif ir == JMP:
            self.pc = self.reg[operand_a]
            continue
        
        elif ir == JEQ:
            if self.FL == 1:
                self.pc = self.reg[operand_a]
                continue
            
        elif ir = JNE:
            if self.FL != 1:
                self.pc = self.reg[operand_a]
                continue
            
        else:
            print('Not working')
            running = False
            
        self.pc += (ir >> 6) + 1
        
    
    
