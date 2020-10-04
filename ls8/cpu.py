"""
LDI Machine code:
```
10000010 00000rrr iiiiiiii
82 0r ii
```

HTL Machine code:
```
00000001 
01
```

PRN Machine code:
```
01000111 00000rrr
47 0r
```

MULT Machine code:
```
10100010 00000aaa 00000bbb
A2 0a 0b
```
"""

"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    # Day 1: Implement the CPU constructor
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256	        
        self.reg[7] = 0xf4
        self.halted = False	  

    # Add RAM functions ram_read()
    def ram_read(self, address):
        """accept the address to read and return the value stored there"""
        return self.ram[address] 

    # Add RAM functions ram_write()
    def ram_write(self, address, value): 
        """accept a value to write, and the address to write it to"""	      
        self.ram[address] = value

    # Day 2: Implement the load() function to load an .ls8 file given the filename passed in as an argument
    def load(self):
        """Load a program into memory."""	      
        address = 0
        
        # For now, we've just hardcoded a program:	       
        program = [	       
            # From print8.ls8	            
            0b10000010,  # LDI R0,8	            
            0b00000000,	            
            0b00001000,	            
            0b01000111,  # PRN R0	          
            0b00000000,	           
            0b00000001,  # HLT	            
        ]
        
        for instruction in program:
            self.ram[address] = instruction	            
            address += 1	            


        # Un-hardcode the machine code
        # if len(sys.argv) != 2:
        #     print('You must have two arguments') 
        #     sys.exit(1)	            
        # try:
        #     with open(sys.argv[1], 'r') as file:  # open 2 files and
        #         # read line by line
        #         for line in file:
        #             # Split the current line on the start of the comment '#' symbol
        #             array_split = line.split('#')
        #             # this removes/strips whitespace and \n character
        #             nums = array_split[0]	                    
        #             try:
        #                 # turn any binary code into a number/integer
        #                 num = int(nums, 2)	     
        #                 # to store into a memory
        #                 self.ram[address] = num
        #                 # moving the array pointer over
        #                 address += 1 	                       
        #             except:
        #                 continue 
                    
        # run python3 ls8.py examples/mult.ls8 
        # otherwise, will get this error message
        # except FileNotFoundError:
        #     print(f"{sys.argv[1]} --> *** File Not Found ***")
            # any number besides 0, it means failed: 2 == FileNotFoundError
            # sys.exit(2)

    # ALU: Arithmetic/Logic Unit - the first part of CPU - the circuitry that performs data manipulation
    def alu(self, op, reg_a, reg_b): 
        """ALU operations."""	    
        
        if op == "ADD":  # 160	
            self.reg[reg_a] += self.reg[reg_b]	    
            # return self.reg[reg_a] 
        # elif op == 162:
        #     self.reg[reg_a] *= self.reg[reg_b]
            # print(self.reg[reg_a])

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


    # Day 1 - Implement the core of CPU's run() method
    def run(self): 
        """Run the CPU."""	       
        # Instruction Register, contains a copy of the currently executing instruction	 
        # if at 160
        # binary representations based on the specs
        LDI = 130
        HLT = 1	        
        PRN = 71	        
        # MULT = 162

        while not self.halted:
            # IR: Instruction Register
            IR = self.ram_read(self.pc)	            
            operand_a = self.ram_read(self.pc + 1)	          
            operand_b = self.ram_read(self.pc + 2)	            

            # Day 1: Add the LDI instruction
            # IR: Instruction Register
            # LDI: Load InDirect - it's used to load a value from a location in memory into a register
            if IR == LDI:
                # reg num is going to have operand:a
                # value is number where we can have the number
                self.reg[operand_a] = operand_b	                
                self.pc += 3
                
            # Day 1: Implement the HALT instruction handler               
            elif IR == HLT:
                self.halted = True	                
                # operating system (1) - exited in a bad way, it failed to do sth. Similar to 500 for a server
                sys.exit(1)
                
            # Day 1: Add the PRINT instruction
            # At this point, I should be able to run the program and have it print 8 to the console!
            elif IR == PRN:
                print(self.reg[operand_a])        
                self.pc += 2
                
                
            # Day 2: Implement a Multiply instruction (run mult.ls8)
            # elif IR == MULT:
            #     self.alu(IR, operand_a, operand_b) #  8 * 9 = 72
            #     self.pc += 3
