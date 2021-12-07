from functools import cache

def parse_input():
    with open("day7/input") as input:
        return [ int(i) for i in input.readline().split(",") ]

positions = parse_input()

def fuel_costs(positions, fuel_cost_moving_to_row):
    min_pos = min(positions)
    max_pos = max(positions)

    return [ fuel_cost_moving_to_row(row, positions) for row in range(min_pos, max_pos + 1)]


def part1():
    def fuel_cost_moving_to_row(row, positions):
        return sum(abs(pos - row) for pos in positions)

    print(f"Part1: {min(fuel_costs(positions, fuel_cost_moving_to_row))}")

def part2():
    @cache
    def cost_for_moving(dist):
        return sum(range(1, dist + 1))

    def fuel_cost_moving_to_row(row, positions):
        return sum(cost_for_moving(abs(pos - row)) for pos in positions)

    print(f"Part2: {min(fuel_costs(positions, fuel_cost_moving_to_row))}")

part2()