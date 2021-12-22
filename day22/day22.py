from dataclasses import dataclass
from itertools import product, tee


@dataclass(frozen=True)
# https://stackoverflow.com/a/25536933
class Brick:
    x_l: int
    x_h: int
    y_l: int
    y_h: int
    z_l: int
    z_h: int

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

        if x_l < x_h and y_l < y_h and z_l < z_h:
            return type(self)(x_l, x_h, y_l, y_h, z_l, z_h)

    def __sub__(self, other):
        assert isinstance(other, Brick)
        other: Brick

        intersection = self & other
        if intersection is None:
            yield self
        else:
            x, y, z = {self.x_l, self.x_h}, {
                self.y_l, self.y_h}, {self.z_l, self.z_h}
            if self.x_l < other.x_l < self.x_h:
                x.add(other.x_l)
            if self.y_l < other.y_l < self.y_h:
                y.add(other.y_l)
            if self.z_l < other.z_l < self.z_h:
                z.add(other.z_l)
            if self.x_l < other.x_h < self.x_h:
                x.add(other.x_h)
            if self.y_l < other.y_h < self.y_h:
                y.add(other.y_h)
            if self.z_l < other.z_h < self.z_h:
                z.add(other.z_h)
            for (x_l, x_h), (y_l, y_h), (z_l, z_h) in product(pairwise(sorted(x)),
                                                              pairwise(
                                                                  sorted(y)),
                                                              pairwise(
                                                                  sorted(z)),
                                                              ):
                instance = type(self)(x_l, x_h, y_l, y_h, z_l, z_h)
                if instance != intersection:
                    yield instance

    def __add__(self, other):
        assert isinstance(other, Brick)
        other: Brick

        intersection = self & other
        if intersection is None:
            yield self
            yield other
        elif intersection == self:
            yield other
        elif intersection == other:
            yield self
        else:
            yield from (self - other)
            yield other

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


def part1():
    def reboot(instructions, limit=50):
        on = set()
        for instruction in instructions:
            (on_off, brick) = instruction
            if on_off == "on":
                on = on | set(brick.cuboids(limit))
            else:
                on = on - set(brick.cuboids(limit))
        return on
    return len(reboot(parse_input("day22/sample")[:2]))


print(f"Part1: {part1()}")


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def part2():
    def reboot(instructions):
        bricks = set()
        for instruction in instructions:
            (on_off, brick) = instruction
            if on_off == "on":
                bricks.add(brick)
            else:
                bricks = reduce(
                    [new_brick for b1 in bricks for new_brick in b1 - brick])
        return reduce(bricks)

    def reduce(bricks):
        while any(b1 & b2 for (b1, b2) in pairwise(bricks)):
            bricks = set(new_brick for (b1, b2) in pairwise(bricks)
                      for new_brick in b1 + b2)
        return bricks

    def sum_volume(bricks):
        #return len(set(cuboid for brick in bricks for cuboid in brick.cuboids()))
        #return bricks
        return sum(brick.volume for brick in bricks)

    return sum_volume(
        reboot(parse_input("day22/sample")[:2])
    )


print(f"Part2: {part2()}")
