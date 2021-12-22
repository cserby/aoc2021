from dataclasses import dataclass
from itertools import permutations, product


class NotABrickException(Exception):
    pass


@dataclass(frozen=True)
# https://stackoverflow.com/a/25536933
class Brick:
    x_l: int
    x_h: int
    y_l: int
    y_h: int
    z_l: int
    z_h: int

    def __post_init__(self):
        if self.x_l > self.x_h:
            raise NotABrickException("x")
        if self.y_l > self.y_h:
            raise NotABrickException("y")
        if self.z_l > self.z_h:
            raise NotABrickException("z")

    def __and__(self, other):
        assert isinstance(other, Brick)
        other: Brick

        x_l, y_l, z_l, x_h, y_h, z_h = \
            max(self.x_l, other.x_l), \
            max(self.y_l, other.y_l), \
            max(self.z_l, other.z_l), \
            min(self.x_h, other.x_h), \
            min(self.y_h, other.y_h), \
            min(self.z_h, other.z_h)

        if x_l <= x_h and y_l <= y_h and z_l <= z_h:
            return type(self)(x_l, x_h, y_l, y_h, z_l, z_h)

    def __sub__(self, other):
        assert isinstance(other, Brick)
        other: Brick

        intersection = self & other
        if intersection is None:
            yield self
        else:
            x_ranges = [
                (self.x_l, intersection.x_l - 1),
                (intersection.x_l, intersection.x_h),
                (intersection.x_h + 1, self.x_h)
            ]
            y_ranges = [
                (self.y_l, intersection.y_l - 1),
                (intersection.y_l, intersection.y_h),
                (intersection.y_h + 1, self.y_h)
            ]
            z_ranges = [
                (self.z_l, intersection.z_l - 1),
                (intersection.z_l, intersection.z_h),
                (intersection.z_h + 1, self.z_h)
            ]
            for (x_range, y_range, z_range) in product(x_ranges, y_ranges, z_ranges):
                (x_l, x_h) = x_range
                (y_l, y_h) = y_range
                (z_l, z_h) = z_range
                try:
                    inst = Brick(x_l, x_h, y_l, y_h, z_l, z_h)
                    if inst != intersection:
                        yield inst
                except NotABrickException:
                    pass

    @property
    def volume(self):
        return (self.x_h - self.x_l + 1) * (self.y_h - self.y_l + 1) * (self.z_h - self.z_l + 1)

    def cuboids(self, limit=50):
        def coord_range(c_r):
            (c_l, c_h) = c_r
            return range(
                max(-1 * limit, c_l) if limit is not None else c_l,
                min(limit, c_h) + 1 if limit is not None else c_h + 1
            )

        for x in coord_range((self.x_l, self.x_h)):
            for y in coord_range((self.y_l, self.y_h)):
                for z in coord_range((self.z_l, self.z_h)):
                    yield (x, y, z)


def parse_input(file="day22/sample"):
    with open(file) as f:
        return [parse_line(line) for line in f.readlines()]


def parse_line(line):
    (on_off, coords) = line.split()
    (x_r, y_r, z_r) = coords.split(",")

    (x_l, x_h) = parse_coord_range(x_r)
    (y_l, y_h) = parse_coord_range(y_r)
    (z_l, z_h) = parse_coord_range(z_r)

    return (on_off, Brick(x_l, x_h, y_l, y_h, z_l, z_h))


def parse_coord_range(coord_range):
    (c_l, c_h) = coord_range.split("=")[1].split("..")
    return (int(c_l), int(c_h))


def reboot(instructions, limit=50):
    on = set()
    for instruction in instructions:
        (on_off, brick) = instruction
        if on_off == "on":
            on = on | set(brick.cuboids(limit))
        else:
            on = on - set(brick.cuboids(limit))
    return on


def part1():
    return len(reboot(parse_input("day22/input"), limit=None))

def minus(brick, bricks):
    remainder = { brick }
    for brick in bricks:
        remainder = { nb for b1 in remainder for nb in b1 - brick }
    return remainder

def reboot_2(instructions):
    bricks = set()
    for instruction in instructions:
        (on_off, brick) = instruction
        if on_off == "on":
            bricks = bricks | set(minus(brick, bricks))
        else:
            bricks = set(new_brick for b1 in bricks for new_brick in b1 - brick)
    return bricks


def sum_volume(bricks):
    if len(bricks) == 0:
        return 0
    else:
        total = sum(brick.volume for brick in bricks)
        pairs = set(permutations(bricks, 2))
        intersections = {i for i in set(
            b1 & b2 for b1, b2 in pairs) if i is not None}
        return total - sum_volume(intersections)


def part2():
    return sum_volume(
        reboot_2(parse_input("day22/input"))
    )


if __name__ == "__main__":
    #print(f"Part1: {part1()}")
    print(f"Part2: {part2()}")
