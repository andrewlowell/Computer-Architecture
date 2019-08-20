"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        byte = 0b00000000
        self.pc = byte
        self.ir = byte
        self.mar = byte
        self.mdr = byte
        self.fl = byte
        self.ram = [byte] * 256
        self.reg = {
          0: byte,
          1: byte,
          2: byte,
          3: byte,
          4: byte,
          5: byte,
          6: byte,
          7: byte
        }


    def ram_read(self, address):
      return self.ram[address]

    def ram_write(self, value, address):
      self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # If no command line argument was provided, exit
        if len(sys.argv) < 2:
          return

        name_of_file_to_load = sys.argv[1]
        program_file = open(name_of_file_to_load)

        for line in program_file:
          if len(line) > 0 and line[0] is not "#":
            self.ram[address] = int(line[0:8], 2)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
          self.reg[reg_a] *= self.reg[reg_b]
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

        running = True
        calling = False
        sp = 0b11110100

        while running:

          self.trace()

          IR = self.ram_read(self.pc)
          operand_a = self.ram_read(self.pc + 1)
          operand_b = self.ram_read(self.pc + 2)

          # HLT
          if IR == 0b00000001:
            running = False

          # LDI
          elif IR == 0b10000010:
            self.reg[operand_a] = operand_b
            self.pc += 3

          #PRN
          elif IR == 0b01000111:
            print(self.reg[operand_a])
            self.pc += 2
          
          # ADD
          elif IR == 0b10100000:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3

          # MUL
          elif IR == 0b10100010:
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3

          # PUSH
          elif IR == 0b01000101:
            # print(f"PUSH self.ram[sp]: {self.ram[sp]}")
            # print(f"register at {operand_a}: {self.reg[operand_a]}")
            self.ram[sp] = self.reg[operand_a]
            sp -= 1
            self.pc += 2
          
          # POP
          elif IR == 0b01000110:
            sp += 1
            # print(f"POP self.ram[sp]: {self.ram[sp]}")
            # print(f"register at {operand_a}: {self.reg[operand_a]}")
            self.reg[operand_a] = self.ram[sp]
            self.pc += 2

          # CALL
          elif IR == 0b01010000:
            self.ram[sp] = self.pc + 2
            self.pc = self.reg[operand_a]
            sp -= 1

          # RET
          elif IR == 0b00010001:
            sp += 1
            self.pc = self.ram[sp]