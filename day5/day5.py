from collections import Counter
#import cProfile

def parse_point(pt):
    return tuple( int(coord) for coord in pt.split(","))

def parse_line(line):
    return [ parse_point(pt) for pt in line.split(" -> ") ]

def parse_input():
    with open("day5/input") as input:
        return [ parse_line(line) for line in input.readlines()]

def expand_non_diagonal_line(line):
    (x1, y1), (x2, y2) = line
    return [ (x, y) for x in range(min(x1, x2), max(x1, x2)+1) for y in range(min(y1, y2), max(y1, y2)+1) ]

def expand_diagonal_line(line):
    (x1, y1), (x2, y2) = line
    slope = int((x1 - x2) / (y1 - y2))
    assert slope == 1 or slope == -1
    intercept = y1 - slope * x1
    return [ (x, slope * x + intercept)
        for x in range(min(x1, x2), max(x1, x2)+1)
    ]

def count_occurrences(lst):
    return Counter(lst)

def overlapping_points(ctr: Counter):
    return [ point for point, count in ctr.items() if count > 1 ]

def horizontal(line):
    (x1, _), (x2, _) = line
    return x1 == x2

def vertical(line):
    (_, y1), (_, y2) = line
    return y1 == y2

def part1():
    lines = parse_input()

    line_points = []
    for line in lines:
        if not (horizontal(line) or vertical(line)):
            continue
        line_points += expand_non_diagonal_line(line)

    point_passes = count_occurrences(line_points)

    overlapping_pts = overlapping_points(point_passes)

    return len(overlapping_pts)

#print(f"Part1: {part1()}")

def part2():
    lines = parse_input()

    line_points = []
    for line in lines:
        line_points += (
            expand_non_diagonal_line(line)
            if horizontal(line) or vertical(line)
            else expand_diagonal_line(line)
        )

    point_passes = count_occurrences(line_points)

    overlapping_pts = overlapping_points(point_passes)

    return len(overlapping_pts)

#cProfile.run("part2()")
print(f"Part2: {part2()}")
