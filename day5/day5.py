from collections import Counter

def parse_point(pt):
    return tuple( int(coord) for coord in pt.split(","))

def parse_line(line):
    return [ parse_point(pt) for pt in line.split(" -> ") ]

def parse_input():
    with open("day5/sample") as input:
        return [ parse_line(line) for line in input.readlines()]

def expand_non_diagonal_line(line):
    (x1, y1), (x2, y2) = line
    return [ (x, y) for x in range(min(x1, x2), max(x1, x2)+1) for y in range(min(y1, y2), max(y1, y2)+1) ]

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

print(f"Part1: {part1()}")