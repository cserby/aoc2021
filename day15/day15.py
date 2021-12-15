#import cProfile

def parse_input():
    with open("day15/input") as input:
        return [[ int(digit) for digit in list(line.strip())] for line in input.readlines() ]

def neighbors(matrix, x, y):
    if x > 0:
        yield (x - 1, y)
    if x < len(matrix) - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < len(matrix[0]) - 1:
        yield (x, y + 1)

def minimal_risks_from_top_left(matrix):
    prev = [[ None for _ in range(len(matrix[0]))] for _ in range(len(matrix)) ]
    risks = [[ None for _ in range(len(matrix[0]))] for _ in range(len(matrix)) ]
    not_visited = { (x, y) for x in range(len(matrix[0])) for y in range(len(matrix)) }

    risks[0][0] = 0

    def is_unvisited(x, y):
        return (x, y) in not_visited

    def min_risk_unvisited():
        min_risk_unvisited = None
        min_risk = None
        for (x, y) in not_visited:
            if min_risk == None:
                min_risk = risks[x][y]
                min_risk_unvisited = (x, y)
            elif risks[x][y] == None:
                continue
            elif min_risk > risks[x][y]:
                min_risk = risks[x][y]
                min_risk_unvisited = (x, y)
            else:
                continue
        return min_risk_unvisited

    while len(not_visited) > 0:
        (x, y) = min_risk_unvisited()
        not_visited.remove((x, y))

        if prev[0][0] == None:
            prev[0][0] = ( -1, -1 )

        for (neighbor_x, neighbor_y) in neighbors(matrix, x, y):
            if not is_unvisited(neighbor_x, neighbor_y):
                continue
            neighbor_risk = risks[neighbor_x][neighbor_y]
            alt = risks[x][y] + matrix[neighbor_x][neighbor_y]
            if neighbor_risk is None or neighbor_risk > alt:
                risks[neighbor_x][neighbor_y] = alt
                prev[neighbor_x][neighbor_y] = (x, y)

    return risks, prev

def part1():
    matrix = parse_input()
    risks, prev = minimal_risks_from_top_left(matrix)
    return risks[-1][-1]

#cProfile.run('part1()')
print(f"Part1: {part1()}")

def increase_cell(cell):
    return (cell - 1) % 9 + 1

def increase_line(line, by):
    return [ increase_cell(cell + by) for cell in line ]

def n_times_line(line, n):
    return [ increase_cell(line[index] + instance) for instance in range(n) for index in range(len(line)) ]

def n_x_n_times(matrix, n):
    matrix_n = [ n_times_line(line, n) for line in matrix ]
    matrix_n_x_n = [ increase_line(matrix_n[index], instance) for instance in range(n) for index in range(len(matrix_n)) ]
    return matrix_n_x_n

def part2():
    matrix = parse_input()
    matrix25 = n_x_n_times(matrix, 5)
    risks, prev = minimal_risks_from_top_left(matrix25)
    return risks[-1][-1]

print(f"Part2: {part2()}")
