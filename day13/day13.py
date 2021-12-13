from itertools import groupby

def parse_input():
    with open("day13/input") as input:
        points, folds = [
            list(lines)
            for empty, lines in groupby((l.strip() for l in input.readlines()), lambda l: l == "")
            if not empty
        ]
        return frozenset(tuple(int(coord) for coord in p.split(",")) for p in points), folds

def fold_x(points, f_x):
    def __fold_x(point, f_x):
        (x, y) = point
        if x > f_x:
            return (f_x - (x - f_x), y)
        else:
            return (x, y)

    return { __fold_x(p, f_x) for p in points }

def fold_y(points, f_y):
    def __fold_y(point, f_y):
        (x, y) = point
        if y > f_y:
            return (x, f_y - (y - f_y))
        else:
            return (x, y)

    return { __fold_y(p, f_y) for p in points }

def fold_on_instruction(points, instruction):
    fold, along, params = instruction.split()
    assert fold == "fold"
    assert along == "along"
    coord, num = params.split("=")
    if coord == "x":
        return fold_x(points, int(num))
    elif coord == "y":
        return fold_y(points, int(num))
    else:
        raise Exception(f"coord: {coord}")

def part1():
    points, folds = parse_input()
    return len(fold_on_instruction(points, folds[0]))

print(f"Part1: {part1()}")