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

def paths(neighbors):
    def paths_from(prefix: List[str], visited: frozenset):
        if prefix[-1] == 'end':
            yield prefix
        else:
            if prefix[-1] == prefix[-1].lower():
                visited = visited | frozenset([prefix[-1]])
            for next in neighbors.get(prefix[-1], frozenset()) - visited:
                yield from paths_from(prefix + [next], visited)

    return [ path for path in paths_from(['start'], frozenset()) ]

def part1():
    return len(paths(build_neighbors(parse_input())))

print(f"Part1: {part1()}")