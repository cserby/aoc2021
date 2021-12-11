from functools import reduce

def parse_input():
    with open("day11/input") as input:
        return [[ int(digit) for digit in list(line.strip())] for line in input.readlines() ]

def neighbors(matrix, x, y):
    if x > 0:
        yield (x - 1, y)
        if y > 0:
            yield(x - 1, y - 1)
    if x < len(matrix) - 1:
        yield (x + 1, y)
        if y < len(matrix[0]) - 1:
            yield (x + 1, y + 1)
    if y > 0:
        yield (x, y - 1)
        if x < len(matrix) - 1:
            yield (x + 1, y - 1)
    if y < len(matrix[0]) - 1:
        yield (x, y + 1)
        if x > 0:
            yield (x - 1, y + 1)

def all_cells(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            yield (x, y)

def count_flashes(flashed):
    add = lambda prev, curr: prev + curr
    return reduce(add, (reduce(add, (1 for flash in line if flash), 0) for line in flashed), 0)

def evolve(matrix):
    flashed = [[ False for _ in range(len(matrix[0]))] for _ in range(len(matrix)) ]

    def check_flash(x, y):
        if matrix[x][y] > 9 and not flashed[x][y]:
            flashed[x][y] = True
            for (n_x, n_y) in neighbors(matrix, x, y):
                matrix[n_x][n_y] += 1
                check_flash(n_x, n_y)

    for (x, y) in all_cells(matrix):
        matrix[x][y] += 1
        check_flash(x, y)

    for (x, y) in all_cells(matrix):
        if matrix[x][y] > 9:
            matrix[x][y] = 0

    return matrix, flashed

def matrix_to_str(matrix):
    matrix_str = ""
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix_str += f"{int(matrix[x][y])}"
        matrix_str += "\n"

    return matrix_str

def after_step(matrix, n):
    return reduce(lambda prev, _: evolve(matrix), range(n), matrix)

matrix_0 = parse_input()

print(f"Step#0: {matrix_0}")
matrix_prev = matrix_0
flash_sum = 0
for step in range(1, 100 + 1):
    print(f"Step#{step}:\n")
    matrix_step, flashed_step = evolve(matrix_prev)
    flash_count = count_flashes(flashed_step)
    print(f"Matrix:\n{matrix_to_str(matrix_step)}Flashed:\n{matrix_to_str(flashed_step)}Flash count: {flash_count}")
    flash_sum += flash_count
    matrix_prev = matrix_step

print(f"Flashes after day 100: {flash_sum}")