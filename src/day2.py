from intcode import Intcode

with open("../input/day2.txt", 'r') as inputFile:
    data = [int(x) for x in inputFile.read().split(",")]

def setInputs(program:list,
              noun: int,
              verb: int):
    program[1] = noun
    program[2] = verb

def handleOp1(program: list,
              src0: int,
              src1: int,
              dest: int):
    #print(f"program[{dest}] = {program[src0]}({src0}) + {program[src1]}({src1})")
    program[dest] = program[src0] + program[src1]
    return 4

def handleOp2(program: list,
              src0: int,
              src1: int,
              dest: int):
    #print(f"program[{dest}] = {program[src0]} * {program[src1]}")
    program[dest] = program[src0] * program[src1]
    return 4

def handleOp99():
    #print("Op99")
    return

# Part 1
part1 = list(data)
setInputs(part1, 12, 2)
runner = Intcode()
print("Part1:", runner.runProgram(part1))

# Part 2
answer = 0
nounPoss = list(range(0, 100))
verbPoss = list(range(0, 100))
shouldBreak = False
for noun in nounPoss:
    for verb in verbPoss:
        part2 = list(data)
        setInputs(part2, noun, verb)
        ret = runner.runProgram(part2)
        if ret == 19690720:
            answer = (100*noun) + verb
            print("Part2:", answer)
            shouldBreak = True
            break
    if shouldBreak:
        break