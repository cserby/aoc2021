from dataclasses import dataclass

@dataclass
class Position:
    horizontal: int
    depth: int

position = Position(0, 0)

def move_forward(n):
    position.horizontal += n

def move_down(n):
    position.depth += n

def move_up(n):
    position.depth -= n

movements = {
    "forward": move_forward,
    "down": move_down,
    "up": move_up,
}

def parse_instruction(line):
    instruction = tuple(line.split(" ", 1))
    return (instruction[0], int(instruction[1]))

def read_instructions():
    with open("day2/input") as input:
        return [ parse_instruction(line) for line in input.readlines()]

def part1():
    instructions = read_instructions()
    for instruction in instructions:
        movements[instruction[0]](instruction[1])
    return position.depth * position.horizontal

print(f"Part1: {part1()}")