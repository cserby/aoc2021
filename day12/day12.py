from typing import List


def parse_input():
    with open("day12/input") as input:
        return [ line.strip().split('-') for line in input.readlines() ]

def add_to_neighbors(neighbors: dict[str, frozenset], point1, point2):
    if point1 not in neighbors.keys():
        neighbors[point1] = frozenset()
    neighbors[point1] = neighbors[point1] | frozenset([point2])
    return neighbors

def build_neighbors(pairs):
    neighbors = dict()
    for (point1, point2) in pairs:
        neighbors = add_to_neighbors(neighbors, point1, point2)
        neighbors = add_to_neighbors(neighbors, point2, point1)
    return neighbors

def paths(neighbors, can_visit_twice = None):
    def paths_from(prefix: List[str], visited: frozenset, can_visit_twice):
        if prefix[-1] == 'end':
            yield prefix
        else:
            if prefix[-1] == prefix[-1].lower() and prefix[-1] != can_visit_twice:
                visited = visited | frozenset([prefix[-1]])
            for next in neighbors.get(prefix[-1], frozenset()) - visited:
                yield from paths_from(
                    prefix + [next],
                    visited,
                    None if prefix[-1] == can_visit_twice else can_visit_twice
                )

    return [ path for path in paths_from(['start'], frozenset(), can_visit_twice) ]

def part1():
    return len(paths(build_neighbors(parse_input())))

print(f"Part1: {part1()}")

def part2():
    neighbors = build_neighbors(parse_input())
    small_caves = [
        key
        for key in neighbors.keys()
        if key == key.lower() and key != 'start' and key != 'end'
    ]
    return len(
        {
            ",".join(path)
            for paths_with_one_small_cave_twice in [
                paths(neighbors, can_visit_twice)
                for can_visit_twice in small_caves
                ]
            for path in paths_with_one_small_cave_twice
        }
    )

print(f"Part2: {part2()}")
