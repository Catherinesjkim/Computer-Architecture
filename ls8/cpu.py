import sys

# Operation Codes = Op Codes
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
PUSH = 0b01000101
POP = 0b01000110

# PC
CALL = 0b01010000 # location in memory where a coroutine starts
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
        # self.ram is a list of 256 zeroes - persistent storage: can store a lot of data 
        self.ram = [0] * 256
        # 8 registers - very few storage - preferred to do for super-fast access
        self.reg = [0] * 8
        self.pc = 0 # PC: Program Counter, address of the currently executing instruction
        # stack pointer is always register 7 - the register that saves the current value - what is the address location? 255 --> 254 --> 253...
        self.sp = 7
        # The flags register FL holds the current flags status. These flags can change based on the operands given to the CMP opcode.
        self.fl = 0

        # Instruction Set: an instruction is a command which tellS the CPU to do some fundamental tasks, such as adding 2 numbers - Op Codes
        self.dispatchable = {
            MUL: self.mul,
            ADD: self.add,
            CMP: self.cmp,
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call, # location in memory where a coroutine starts
            RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }

    # Day 2 - Implement the load() function to load an .ls8 file given the filename passed in as an argument
    # Un-hardcode the machine code
    def load(self, file_name):
        address = 0
        
        # Day 3 - command line arguments: python3 [ls8.py examples/stack.ls8]
        # open/traverse a file and load into memory
        with open(file_name, 'r') as file:  # open 2 files
            # read line by line
            for line in file:
                print(line)
                # ignore the '#' and white spaces
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
    # MAR: Memory Address Register, holds the memory address we're reading or writing
    def ram_read(self, mar):
        return self.ram[mar]

    # Day 1: Write a value at given address
    # MDR: Memory Data Register, holds the value to write or the value just read
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
        self.alu("MUL", reg_a, reg_b)  # 8 * 9 = 72 (output)
        self.pc += 3 

    # Day 1: Implement an Add instruction (run mult.ls8)
    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    # Handle CMP with Equal flag
    # Compare is the same as subtraction except that the result value is not stored - handled by ALU
    # Compare the values in two registers.
    # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
    # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
    # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
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

    # Day 3: Implement the System Stack and be able to run the stack.ls8 program with PUSH
    def push(self, reg_a, reg_b):
        # decreement the stack pointer
        self.sp -= 1
        # write the value of the given register to memory AT the SP location
        self.ram_write(self.sp, self.reg[reg_a])
        self.pc += 2

     # Day 3: Implement the System Stack and be able to run the stack.ls8 program with POP
    def pop(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    # Day 4: CALL takes a register - calls a subroutine (function) at the address stored in the register
    # 1. The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing
    # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC moves forward and backwards from its current location
        # Pop from stack and set PC to the value
    # CALL: Location in memory where corouting starts
    def call(self, reg_a, reg_b):
        # Get the given register in the operand
        # decrement the Stack Pointer
        self.sp -= 1
        # Store the return address (PC + 2) onto the stack
        # write the return address 
        self.ram_write(self.sp, self.pc + 2)
        # SET PC To the value inside given_register
        # Move pc to location given by register & store the Return address in the Stack
        # pc equals to registers at given register
        self.pc = self.reg[reg_a]

    # Day 4: RET is listed as a separate instruction in the spec, since it's different keyword in assembly. It's a speical case of JMP. RET happens whenever R1 is 7
    # Pop from stack and set PC to the value
    def ret(self, reg_a, reg_b):
        # sest PC to the value at the top of the stack
        self.pc = self.ram_read(self.sp)
        # POP from stack - move it back up (grows downwards)
        self.sp += 1

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
            # IR: Instruction Register contains a copy of the currently executing instruction
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            # Day 1: Implement the HLT Halt instruction handler
            if ir == HLT:
                running = False
            else:
                self.dispatchable[ir](reg_a, reg_b)
