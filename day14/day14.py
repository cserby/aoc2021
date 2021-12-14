from itertools import groupby
from functools import reduce
from typing import Counter


def parse_patterns(patterns):
    def parse_patterns_generator():
        for pattern in patterns:
            [match, replace] = pattern.split(" -> ")
            yield match, replace

    matches, patterns = zip(*(parse_patterns_generator()))
    return dict( zip( matches, patterns ))

def parse_input():
    with open("day14/input") as input:
        template, patterns = [
            list(lines)
            for empty, lines in groupby((l.strip() for l in input.readlines()), lambda l: l == "")
            if not empty
        ]
        assert len(template) == 1
        return template[0], parse_patterns(patterns)

def pairs(template):
    for i in range(len(template) - 1):
        yield template[i:i+2]

def evolve(template, patterns):
    new_template = template[0]
    for pair in pairs(template):
        if pair in patterns.keys():
            new_template = new_template + patterns[pair] + pair[1]
        else:
            new_template += pair
    return new_template

def after_step(step, template, patterns):
    return reduce(lambda prev, _: evolve(prev, patterns), range(step), template)

def part1():
    template, patterns = parse_input()
    counter = Counter(after_step(10, template, patterns))
    return max(counter.values()) - min(counter.values())

print(f"Part1: {part1()}")