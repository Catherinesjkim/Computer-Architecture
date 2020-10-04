"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256	        
        self.reg[7] = 0xf4
        self.halted = False	  

    def ram_read(self, address):
        """accept the address to read and return the value stored there"""
        return self.ram[address] 

    def ram_write(self, address, value): 
        """accept a value to write, and the address to write it to"""	      
        self.ram[address] = value

    # Day 2: Implement the load() function to load an .ls8 file given the filename passed in as an argument
    def load(self):
        """Load a program into memory."""	      
        address = 0	        
        if len(sys.argv) != 2:
            print('You must have two arguments') 
            sys.exit(1)	            
        try:
            with open(sys.argv[1], 'r') as file:
                for line in file:
                    array_split = line.split('#')	                
                    nums = array_split[0]	                    
                    try:
                        num = int(nums, 2)	                        
                        self.ram[address] = num	                       
                        address += 1 	                       
                    except:
                        continue 
        except:
            print("File not found") 
            sys.exit(1)	            

    def alu(self, op, reg_a, reg_b): 
        """ALU operations."""	    

        if op == "ADD":  # 160	
            self.reg[reg_a] += self.reg[reg_b]	    
            return self.reg[reg_a] 
        elif op == 162:
            self.reg[reg_a] *= self.reg[reg_b]
            print(self.reg[reg_a])

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

    # Day 2 - Step 3: Implement the core of CPU's run() method
    def run(self): 
        """Run the CPU."""	       
        # Instruction Register, contains a copy of the currently executing instruction	 
        # if at 160	        
        LDI = 130	       
        HLT = 1	        
        PRN = 71	        
        MULT = 162

        while not self.halted:
            # IR: Instruction Register
            IR = self.ram_read(self.pc)	            
            operand_a = self.ram_read(self.pc + 1)	          
            operand_b = self.ram_read(self.pc + 2)	            

            # Step 5: Add the LDI instruction
            # IR: Instruction Register
            # LDI: Load InDirect - it's used to load a value from a location in memory into a register
            if IR == LDI:
                print("in here")
                # reg num is going to have operand:a
                # value is number where we can have the number
                self.reg[operand_a] = operand_b	                
                self.pc += 3	                
            elif IR == HLT:
                self.halted = True	                
                sys.exit(1)
            # Step 6: Add the PRN instruction
            # At this point, I should be able to run the program and have it print 8 to the console!
            elif IR == PRN:
                print(self.reg[operand_a])	                
                self.pc += 2
                
            # Day 2: Implement a Multiply instruction (run mult.ls8)
            elif IR == MULT:
                self.alu(IR, operand_a, operand_b) #  8 * 9 = 72
                self.pc += 3
