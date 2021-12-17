from itertools import islice


def parse_input():
    with open("day17/input") as input:
        line = input.readline().strip()
        parts = line.split(" ")
        x_range_low, x_range_high = [ int(range) for range in parts[-2][2:-1].split("..") ]
        y_range_low, y_range_high = [ int(range) for range in parts[-1][2:].split("..") ]
        return ((x_range_low, x_range_high), (y_range_low, y_range_high))

def trajectory(v_x0, v_y0):
    v_x, v_y = v_x0, v_y0
    x, y = (0, 0)
    while True:
        x, y = x + v_x, y + v_y
        yield ((x, y), (v_x, v_y))
        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1
        v_y -= 1

def take(iterable, n):
    return [ item for item in islice(iterable, n) ]

def take_while(iterable, check):
    try:
        while True:
            item = next(iterable)
            if check(item):
                yield item
            else:
                return
    except StopIteration:
        pass

def hit(curr, target_range):
    (x_range_low, x_range_high), (y_range_low, y_range_high) = target_range
    ((x, y), _) = curr

    return x_range_low <= x and x <= x_range_high and y_range_low <= y and y <= y_range_high

def impossible_hit(curr, target_range):
    (x_range_low, x_range_high), (y_range_low, y_range_high) = target_range
    ((x, y), (v_x, v_y)) = curr

    if y < y_range_low:
        return True
    if x < x_range_low and v_x <= 0:
        return True
    if x > x_range_high and v_x >= 0:
        return True
    else:
        return False

def evaluate_trajectory(trajectory, target_range):
    try:
        return hit(list(trajectory)[-1], target_range)
    except IndexError:
        return False

def trajectories_on_target(target_range):
    (x_range_low, x_range_high), (y_range_low, y_range_high) = target_range
    # TODO Why these ranges?
    for v_x in range(0, x_range_high + 1):
        for v_y in range(y_range_low - 1, 100):
            traj = list(take_while(trajectory(v_x, v_y), lambda curr: not impossible_hit(curr, target_range)))
            if evaluate_trajectory(traj, target_range):
                yield traj

def max_y(trajectory):
    return max([ y for ((_, y), _) in trajectory ])

def max_ys(trajectories):
    return max([ max_y(trajectory) for trajectory in trajectories ])

def part1():
    target_range = parse_input()
    on_target = list(trajectories_on_target(target_range))
    return max_ys(on_target)

print(f"Part1: {part1()}")

def part2():
    target_range = parse_input()
    on_target = list(trajectories_on_target(target_range))
    return len([ traj[0][1] for traj in on_target ])

print(f"Part2: {part2()}")
