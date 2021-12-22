def parse_input(file="day22/sample"):
    with open(file) as f:
        return [parse_line(line) for line in f.readlines()]


def parse_line(line):
    (on_off, coords) = line.split()
    (x_r, y_r, z_r) = coords.split(",")

    (x_l, x_h) = parse_coord_range(x_r)
    (y_l, y_h) = parse_coord_range(y_r)
    (z_l, z_h) = parse_coord_range(z_r)

    return (on_off, (x_l, x_h), (y_l, y_h), (z_l, z_h))


def parse_coord_range(coord_range):
    (c_l, c_h) = coord_range.split("=")[1].split("..")
    return (int(c_l), int(c_h))


def cuboids(x_r, y_r, z_r, limit=50):
    def coord_range(c_r):
        (c_l, c_h) = c_r
        return range(
            max(-1 * limit, c_l) if limit is not None else c_l,
            min(limit, c_h) + 1 if limit is not None else c_h + 1
        )

    for x in coord_range(x_r):
        for y in coord_range(y_r):
            for z in coord_range(z_r):
                yield (x, y, z)


def reboot(instructions, limit=50):
    on = set()
    for instruction in instructions:
        (on_off, x_r, y_r, z_r) = instruction
        if on_off == "on":
            on = on | set(cuboids(x_r, y_r, z_r, limit))
        else:
            on = on - set(cuboids(x_r, y_r, z_r, limit))
    return on


def part1():
    return len(reboot(parse_input("day22/input")))


print(f"Part1: {part1()}")

def part2():
    return len(reboot(parse_input("day22/sample"), limit=None))

print(f"Part2: {part2()}")