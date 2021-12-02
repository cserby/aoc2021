from dataclasses import dataclass

@dataclass
class Position:
    horizontal: int
    depth: int
    aim: int

def parse_instruction(line):
    instruction = tuple(line.split(" ", 1))
    return (instruction[0], int(instruction[1]))

def read_instructions():
    with open("day2/input") as input:
        return [ parse_instruction(line) for line in input.readlines()]

instructions = read_instructions()

def part1():
    position = Position(0, 0, 0)

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

    for instruction in instructions:
        movements[instruction[0]](instruction[1])
    return position.depth * position.horizontal

def part2():
    position = Position(0, 0, 0)

    def move_forward(n):
        position.horizontal += n
        position.depth += n * position.aim

    def move_down(n):
        position.aim += n

    def move_up(n):
        position.aim -= n

    movements = {
        "forward": move_forward,
        "down": move_down,
        "up": move_up,
    }

    for instruction in instructions:
        movements[instruction[0]](instruction[1])
    return position.depth * position.horizontal

print(f"Part1: {part1()}")
print(f"Part2: {part2()}")