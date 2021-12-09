from math import prod

def parse_input():
    with open("day9/input") as input:
        return [[ int(digit) for digit in list(line.strip())] for line in input.readlines() ]

def safe_list_get(list, index, default):
    if index < 0:
        return default
    try:
        return list[index]
    except IndexError:
        return default

def cell(matrix, x, y):
    return safe_list_get(safe_list_get(matrix, x, []), y, None)

def neighbors(matrix, x, y):
    if x > 0:
        yield (x - 1, y)
    if x < len(matrix) - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < len(matrix[0]) - 1:
        yield (x, y + 1)

def neighbor_values(matrix, x, y):
    return [ cell(matrix, x, y) for (x, y) in neighbors(matrix, x, y) ]

def local_minimum(matrix, x, y):
    return all(cell(matrix, x, y) < n for n in neighbor_values(matrix, x, y))

def local_minimums(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if local_minimum(matrix, x, y):
                yield (x, y, cell(matrix, x, y))

def local_minimum_risks(matrix):
    return [ c + 1 for (x, y, c) in local_minimums(matrix) ]

def part1():
    matrix = parse_input()
    return sum(local_minimum_risks(matrix))

print(f"Part1: {part1()}")

def write_cell(matrix, x, y, value):
    matrix[x][y] = value
    return matrix

def basin_sizes(matrix):
    visited = [[ False for _ in range(len(matrix[0]))] for _ in range(len(matrix)) ]

    def unvisited():
        for x in range(len(visited)):
            for y in range(len(visited[0])):
                if not cell(visited, x, y):
                    yield (x, y)

    def basin_size(matrix, x, y):
        need_to_go = {(x, y)}
        basin_size = 0
        while len(need_to_go) > 0:
            (visiting_x, visiting_y) = need_to_go.pop()
            if cell(visited, visiting_x, visiting_y):
                continue
            else:
                write_cell(visited, visiting_x, visiting_y, True)
                if cell(matrix, visiting_x, visiting_y) == 9:
                    continue
                else:
                    basin_size += 1
                    need_to_go = need_to_go | set(neighbors(matrix, visiting_x, visiting_y))
        return basin_size

    for (x, y) in unvisited():
        yield basin_size(matrix, x, y)

def part2():
    matrix = parse_input()
    return prod(sorted(list(basin_sizes(matrix)), reverse=True)[:3])

print(f"Basin size: {part2()}")