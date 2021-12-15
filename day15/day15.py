import cProfile

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
    risks = dict()
    not_visited = { (x, y) for x in range(len(matrix[0])) for y in range(len(matrix)) }

    risks[(0, 0)] = 0
    frontier = { (0, 0) }

    def min_risk_on_frontier():
        risks_unvisited = { coord: risks[coord] for coord in frontier }
        return min(risks_unvisited, key=risks_unvisited.get)

    while len(not_visited) > 0:
        (x, y) = min_risk_on_frontier()
        not_visited.remove((x, y))

        frontier.remove((x, y))
        frontier = frontier | set(coord for coord in neighbors(matrix, x, y) if coord in not_visited)

        for (neighbor_x, neighbor_y) in neighbors(matrix, x, y):
            if (neighbor_x, neighbor_y) not in not_visited:
                continue
            alt = risks[(x, y)] + matrix[neighbor_x][neighbor_y]
            neighbor_risk = risks.get((neighbor_x, neighbor_y), None)
            if neighbor_risk is None or neighbor_risk > alt:
                risks[(neighbor_x, neighbor_y)] = alt

    return risks

def part1():
    matrix = parse_input()
    risks = minimal_risks_from_top_left(matrix)
    return risks[(len(matrix) - 1, len(matrix[-1]) - 1)]

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

def part2(n = 5):
    matrix = parse_input()
    matrix25 = n_x_n_times(matrix, n)
    risks = minimal_risks_from_top_left(matrix25)
    return risks[(len(matrix25) - 1, len(matrix25[-1]) - 1)]

print(f"Part2: {part2()}")
#cProfile.run('part2(2)')