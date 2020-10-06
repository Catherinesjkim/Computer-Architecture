import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
# PUSH = 0b01000101
# POP = 0b01000110

# PC
CALL = 0b01010000
RET = 0b00010001
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

# ALU
MUL = 0b10100010
ADD = 0b10100000
CMP = 0b10100111


# Main CPU class
class CPU:
    # Day 1: Construct a new CPU
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7  # stack pointer is always register 7
        self.fl = 0

        self.dispatchable = {
            MUL: self.mul,
            ADD: self.add,
            CMP: self.cmp,
            PRN: self.prn,
            LDI: self.ldi,
            # PUSH: self.push,
            # POP: self.pop,
            # CALL: self.call,
            # RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }

    # Day 2 - Implement the load() function to load an .ls8 file given the filename passed in as an argument
    # Un-hardcode the machine code
    # Implement the load() function to load an .ls8 file given the filename passed in as an argument
    def load(self, file_name):
        address = 0

        with open(file_name, 'r') as file:  # open 2 files and
            # read line by line
            for line in file:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    # Split the current line on the start of the empty ' ' space
                    instruction = line.split(' ')[0]
                    # turn any binary code into a number/integer
                    self.ram[address] = int(instruction, 2)
                    # moving the array pointer over
                    address += 1

    # Da1 1: Read RAM at given address and return that value
    def ram_read(self, mar):
        return self.ram[mar]

    # Day 1: Write a value at given address
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # ALU operations
    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # Day 2
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.fl = 1 if self.reg[reg_a] == self.reg[reg_b] else 0
        else:
            raise Exception("Unsupported ALU operation")

    # Handy function to print out the CPU state.
    # You might want to call this from run() if you need help debugging.
    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # Day 2: Implement a Multiply instruction (run mult.ls8)
    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)  # 8 * 9 = 72
        self.pc += 3 

    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    # Handle CMP with Equal flag
    # Compare is the same as subtraction except that the result value is not stored - handled by ALU
    def cmp(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    # Day 1: Add the PRN Print instruction
    def prn(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2

    # Day 1: Add the LDI Load instruction
    def ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3

    # def push(self, reg_a, reg_b):
    #     self.sp -= 1
    #     self.ram_write(self.sp, self.reg[reg_a])
    #     self.pc += 2

    # def pop(self, reg_a, reg_b):
    #     self.reg[reg_a] = self.ram_read(self.sp)
    #     self.sp += 1
    #     self.pc += 2

    # def call(self, reg_a, reg_b):
    #     self.sp -= 1
    #     self.ram_write(self.sp, self.pc + 2)
    #     self.pc = self.reg[reg_a]

    # def ret(self, reg_a, reg_b):
    #     self.pc = self.ram_read(self.sp)
    #     self.sp += 1

    # Jump register. Jump to the address stored in the given register. Set the PC to the address stored in the given register.
    def jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]

    # JEQ register. If equal flag is set(true), jump to the address stored in the given register
    def jeq(self, reg_a, reg_b):
        if self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2

    # JNE register. If E flag is clear (false, 0), jump to the address stored in the given register. Jump if Condition is Met - conditional jump that follows a test - it's commonly found after a CMP instruction
    def jne(self, reg_a, reg_b):
        if not self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2

    # Day 1: Implement the core of run()
    # Run the CPU
    def run(self):
        running = True

        while running:
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            # Day 1: Implement the HLT Halt instruction handler
            if ir == HLT:
                running = False
            else:
                self.dispatchable[ir](reg_a, reg_b)
