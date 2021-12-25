
def parse_input():
    with open("day25/input") as input:
        return [[ char for char in list(line.strip())] for line in input.readlines() ]

def step(matrix):
    return step_down(step_right(matrix))

def step_right(matrix):
    return [ step_right_line(line) for line in matrix ]

def step_right_line(line):
    new_line = list(line)
    for i in range(len(line)):
        if line[ i ] == '>' and line[ (i+1) % len(line) ] == '.':
            new_line[ i ] = '.'
            new_line[ (i+1) % len(line) ] = '>'

    return new_line

def indices(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            yield x, y

def step_down(matrix):
    new_matrix = [ list(line) for line in matrix ]

    for x, y in indices(matrix):
        if matrix[x][y] == 'v' and matrix[ (x+1) % len(matrix) ][y] == '.':
            new_matrix[x][y] = '.'
            new_matrix[ (x+1) % len(matrix) ][y] = 'v'
    return new_matrix

def part1():
    matrix = parse_input()
    step_count = 0

    while True:
        from pprint import pprint
        #print(f"STEP {step_count}")
        #pprint(matrix)
        #print()

        new_matrix = step(matrix)
        step_count += 1

        if new_matrix == matrix:
            return step_count
        else:
            matrix = new_matrix

print(f"Part1: {part1()}")