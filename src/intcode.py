from enum import Enum

class ParameterMode(Enum):
    Position  = 0
    Immediate = 1

class Intcode():
    def __init__(self, verbose=False):
        self.verbose     = verbose
        self.program     = []
        self.inputStream = []
        self.ip      = 0
        self.eop     = False
        self.retVal = None
        self.opcodes = {
            1 : self.opcode1,
            2 : self.opcode2,
            3 : self.opcode3,
            4 : self.opcode4,
            5 : self.opcode5,
            6 : self.opcode6,
            7 : self.opcode7,
            8 : self.opcode8,
            99: self.opcode99
        }

    def runProgram(self, program: list, inputStream: list = []):
        self.program     = list(program)
        self.ip          = 0
        self.eop         = False
        self.inputStream = inputStream
        self.retVal      = None

        while self.eop is False:
            if self.verbose: print(f"IP: {self.ip} - ", end='')
            instruction = "00000000000000" + str(self.program[self.ip])
            opcode      = int(instruction[-2:])
            if opcode in self.opcodes:
                self.opcodes[opcode]([int(x) for x in instruction[:-2]])

        return self.retVal

    def getOperand(self, operand: int, modes: list):
        value = self.program[self.ip + operand]
        mode  = ParameterMode(modes[-operand])
        if mode == ParameterMode.Position:
            return self.program[value]
        elif mode == ParameterMode.Immediate:
            return value

    def opcode1(self, modes: list):
        src0 = self.getOperand(1, modes)
        src1 = self.getOperand(2, modes)
        dest = self.program[self.ip + 3]
        if self.verbose:
            print(f"program[{dest}] = {src0}({self.program[self.ip + 1]}) + {src1}({self.program[self.ip + 2]})")
        self.program[dest] = src0 + src1
        self.ip += 4

    def opcode2(self, modes: list):
        src0 = self.getOperand(1, modes)
        src1 = self.getOperand(2, modes)
        dest = self.program[self.ip + 3]
        if self.verbose:
            print(f"program[{dest}] = {src0}({self.program[self.ip + 1]}) * {src1}({self.program[self.ip + 2]})")
        self.program[dest] = src0 * src1
        self.ip += 4

    def opcode3(self, modes: list):
        dest  = self.program[self.ip + 1]
        assert(len(self.inputStream) > 0)
        value = int(self.inputStream.pop(0))
        if self.verbose:
            print(f"program[{dest}] = {value}")
        self.program[dest] = value
        self.ip += 2

    def opcode4(self, modes: list):
        src0 = self.getOperand(1, modes)
        if self.verbose:
            print(f"Output: {src0}")
        self.retVal = src0
        self.ip += 2

    def opcode5(self, modes: list):
        src0    = self.getOperand(1, modes)
        jumpLoc = self.getOperand(2, modes)
        if self.verbose:
            print(f"jump-if-true - src0({src0}), destIp({jumpLoc})")
        if src0 != 0:
            self.ip = jumpLoc
        else:
            self.ip += 3

    def opcode6(self, modes: list):
        src0    = self.getOperand(1, modes)
        jumpLoc = self.getOperand(2, modes)
        if self.verbose:
            print(f"jump-if-false - src0({src0}), destIp({jumpLoc})")
        if src0 == 0:
            self.ip = jumpLoc
        else:
            self.ip += 3

    def opcode7(self, modes: list):
        src0    = self.getOperand(1, modes)
        src1    = self.getOperand(2, modes)
        dest    = self.program[self.ip + 3]
        if self.verbose:
            print(f"less-than - program[{dest}] = 1 if {src0}({self.program[self.ip + 1]}) < {src1}({self.program[self.ip + 2]}) else 0")
        self.program[dest] = 1 if src0 < src1 else 0
        self.ip += 4

    def opcode8(self, modes: list):
        src0    = self.getOperand(1, modes)
        src1    = self.getOperand(2, modes)
        dest    = self.program[self.ip + 3]
        if self.verbose:
            print(f"less-than - program[{dest}] = 1 if {src0}({self.program[self.ip + 1]}) == {src1}({self.program[self.ip + 2]}) else 0")
        self.program[dest] = 1 if src0 == src1 else 0
        self.ip += 4


    def opcode99(self, modes: list):
        self.ip  += 1
        self.eop  = True

        if self.retVal is None:
            self.retVal = self.program[0]

