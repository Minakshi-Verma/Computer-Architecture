"""CPU functionality."""

import sys
sp =7 # reference for stack pointer (stored at registor 7)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""        
        self.ram= [0]* 256   #  hold 256 bytes of memory
        self.reg =[0]*8      #  hold 8 general-purpose registers
        self.pc = 0          # program counter 

        self.reg[sp] = 0xF4 #OR self.reg[7] = 0xf4    # sp pointer at the  
                            #address 0xF4 (if stack is empty) and its address is stored at registor 7

        self.equal= 0
        self.lesser= 0
        self.greater = 0
        
    
    #ram_read() that accepts the address to read and return the value stored there.
    # Memory Address Register (MAR)
    def ram_read(self, mar):
        return self.ram[mar]
    
    #ram_write() that accepts a value to write, and the address to write it to.
    # Memory Address Register (MAR) and the Memory Data Register (MDR)
    def ram_write(self, mar,mdr):
        self.ram[mar] = mdr

    
    def load(self,prog):
        """Load a program into memory."""

        # address = 0
        try:  
            address = 0    
            with open(prog) as program:
                for line in program:
                    split_line = line.split('#')[0]                   
                    command = split_line.strip()
                    # print(type(command))
                    # print(command)

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    # self.ram[address] = instruction
                    self.ram_write(address ,instruction)
                    # print(instruction)            

                    address += 1      

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    if len(sys.argv) < 2:
        print("Please pass in a second filename: python3 ls8.py second_filename.py")
        sys.exit()

    # prog = sys.argv[1]
   
        #-----------------
    # Our previous hard coded load function

    #  def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]

    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1
            #________________
        

    
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # if ALU operation is ADD
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        #if ALU operation is MULTIPLY(MUL)
        elif op == "MUL":
            product = self.reg[reg_a]*self.reg[reg_b]
            self.reg[reg_a] = product
        
        #if ALU operation id COMPARE(CMP)
        elif op == "CMP":
            if self.reg[reg_a]== self.reg[reg_b]:
                self.equal =1
            if self.reg[reg_a]< self.reg[reg_b]:
                self.lesser =1
            if self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1

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

    def run(self):
        """Run the CPU."""
        #machine codes--opcode       
        
        LDI = 0b10000010   # opcode1, This instruction sets a specified register to a specified value(List data item), takes only 1 operand( determine from 1st 2 values)
        PRN = 0b01000111   #opcode2, Print numeric decimal integer value that is stored in the given register
        HLT = 0b00000001   #opcode 3, Halt the CPU (and exit the emulator).
        MUL =  0b10100010  # opcode 4, multiply the values in two resistors and store the value in registerA  
        PUSH = 0b01000101 #Push the value in the given register on the stack.
        POP = 0b01000110 #Pop the value at the top of the stack into the given register
        CALL= 0b01010000 #Calls a subroutine (function) at the address stored in the register. 
        RET= 0b00010001 #Return from subroutine  
        ADD = 0b10100000
      
        running = True

        while running:
            command = self.ram_read(self.pc)
           
            operand_a = self.ram_read(self.pc+1)  # variable 1(address)
            operand_b = self.ram_read(self.pc+2)   # variable 2(value)
                    
            if command == HLT:
                # exit the running operation
                running = False
                self.pc +=1

            elif command == LDI:              
                # sets the value of register to an integer                
                self.reg[operand_a]= operand_b
                self.pc +=3

            elif command == PRN:
                print(self.reg[operand_a])
                self.pc +=2

            elif command ==MUL:               
                # num1 = self.reg[operand_a]
                # num2 = self.reg[operand_b]
                # product = num1* num2
                # self.reg[operand_a]= product
                # self.pc +=3  

                #Using ALU
                self.alu("MUL", operand_a,operand_b) 
                self.pc +=3      

            elif command ==PUSH:
                #decrement the stack pointer (sp)
                self.reg[sp] -=1

                #get the value from address of register(operand_a) 
                data_to_push = self.reg[operand_a]              

                #write/push the value at stack pointer(SP)address                              
                self.ram_write(self.reg[sp],data_to_push)

                #increment the program counter(pc)
                self.pc +=2

            elif command ==POP:
                #get the stack pointer (where do we look?)
                # get/read register number to put value in
                value = self.ram_read(self.reg[sp])              

                # increment the stack pointer
                self.reg[sp] +=1             
                
                # put the value into the given register
                self.reg[operand_a] = value
                #increment the program counter(pc)
                self.pc +=2

            elif command ==ADD:
                added = self.reg[operand_a]+self.reg[operand_b]
                self.reg[operand_a] = added
                self.pc +=3

                #using ALU() 
                # self.alu("ADD",operand_a,operand_b)
                # self.pc +=3
            
            elif command ==CALL:
                # next instruction address poped and stored/pushed in the stack
                # decrement Stack Pointer(since we are pushing on stack) 
                self.reg[sp] -=1
                #The next instruction is poped and stored on stack(call is 2 bytes intruction so pc+2)
                self.ram[self.reg[sp]]=self.pc + 2
                
               # PC pointer goes to subroutine(ADD in this case)                
                self.pc= self.reg[operand_a]

            elif command == RET:
                # pops the stack and bring that instruction back where it was and store the value on PC (to run next)
                self.pc=self.ram[self.reg[sp]]
                # increment the stack pointer after pop
                self.reg[sp] +=1

            

           

                



