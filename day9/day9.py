def parse_input():
    with open("day9/input") as input:
        return [[ int(digit) for digit in list(line.strip())] for line in input.readlines() ]

def safe_list_get(list, index, default):
    try:
        return list[index]
    except IndexError:
        return default

def cell(matrix, x, y):
    return safe_list_get(safe_list_get(matrix, x, []), y, None)

def neighbors(matrix, x, y):
    return [ c for c in [ cell(matrix, x-1, y), cell(matrix, x+1, y), cell(matrix, x, y-1), cell(matrix, x, y+1)] if c is not None ]

def local_minimum(matrix, x, y):
    return all(cell(matrix, x, y) < n for n in neighbors(matrix, x, y))

def local_minimums(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if local_minimum(matrix, x, y):
                yield (x, y, cell(matrix, x, y))

def local_minimum_risks(matrix):
    return [ c + 1 for (x, y, c) in local_minimums(matrix) ]

def part1():
    matrix = parse_input()
    print(f"Part1: {sum(local_minimum_risks(matrix))}")

part1()
