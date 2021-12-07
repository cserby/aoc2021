def parse_input():
    with open("day7/input") as input:
        return [ int(i) for i in input.readline().split(",") ]

positions = parse_input()

def fuel_cost_moving_to_row(row, positions):
    return sum(abs(pos - row) for pos in positions)

def fuel_costs(positions):
    min_pos = min(positions)
    max_pos = max(positions)

    return [ fuel_cost_moving_to_row(row, positions) for row in range(min_pos, max_pos + 1)]

print(min(fuel_costs(positions)))
