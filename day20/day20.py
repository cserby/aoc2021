from functools import cache
from itertools import groupby
from typing import List


def parse_input():
    with open("day20/input") as input:
        algo, img = [
            list(lines)
            for empty, lines in groupby((l.strip() for l in input.readlines()), lambda l: l == "")
            if not empty
        ]
        return algo[0], list(list(line) for line in img)


def pixel(image, step, pixel):
    (x, y) = pixel

    try:
        if x < 0 or y < 0:
            raise IndexError((x, y))
        return image[x][y]
    except IndexError:
        # TODO depends on step!
        return '.' if step % 2 == 0 else '#'


def pixels(image):
    for x in range(len(image)):
        for y in range(len(image[0])):
            yield (x, y)


def neighbors(pixel):
    (x, y) = pixel
    yield from [(x_p, y_p) for x_p in range(x-1, x+2) for y_p in range(y-1, y+2)]


def neighborhood(image, step, px):
    return "".join(pixel(image, step, pos) for pos in neighbors(px))


def to_int(neighborhd: str):
    return int(neighborhd.replace(".", "0").replace("#", "1"), 2)


def replacement(algo, image, step, px):
    return algo[to_int(neighborhood(image, step, px))]


def next_image(image, step):
    return [
        [
            replacement(algo, image, step, (x, y)) for y in range(-2, len(image[0]) + 3)
        ] for x in range(-2, len(image) + 3)
    ]


def count_light(image):
    return sum([1 for px in pixels(image) if pixel(image, 0, px) == '#'])

def display(image):
    for line in image:
        for cell in line:
            print(cell, end='')
        print()

def image_after_step(image, step):
    curr_image = image
    for curr_step in range(step, 0, -1):
        curr_image = next_image(curr_image, curr_step)
    return curr_image


algo, image = parse_input()

def part1():
    return count_light(image_after_step(image, 2))

print(f"Part1: {part1()}")

def part2():
    return count_light(image_after_step(image, 50))

print(f"Part2: {part2()}")