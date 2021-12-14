from functools import reduce
from itertools import groupby
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

def most_common_minus_least_common(counter):
    return max(counter.values()) - min(counter.values())

def part1():
    template, patterns = parse_input()
    return most_common_minus_least_common(Counter(after_step(10, template, patterns)))

print(f"Part1: {part1()}")

def evolve_pairs(pair_counts, patterns):
    new_pair_counts = {**pair_counts}
    for pair in pair_counts.keys():
        if pair in patterns.keys():
            try:
                new_pair_counts[pair[0] + patterns[pair]] += pair_counts[pair]
            except KeyError:
                new_pair_counts[pair[0] + patterns[pair]] = pair_counts[pair]
            try:
                new_pair_counts[patterns[pair] + pair[1]] += pair_counts[pair]
            except KeyError:
                new_pair_counts[patterns[pair] + pair[1]] = pair_counts[pair]
            new_pair_counts[pair] -= pair_counts[pair]
    return new_pair_counts

def pairs_after_step(step, template, patterns):
    return reduce(lambda prev, _: evolve_pairs(prev, patterns), range(step), Counter(pairs(template)))

# To avoid duplication, for each pair it counts the first element
# This'll leave unaccounted for the last element in the polymer!
def count_elements_except_last(pair_counter):
    element_counter = dict()
    for pair in pair_counter.keys():
        try:
            element_counter[pair[0]] += pair_counter[pair]
        except KeyError:
            element_counter[pair[0]] = pair_counter[pair]
    return element_counter

def part2():
    template, patterns = parse_input()
    return most_common_minus_least_common({
        # Compensate for the last element in the counts
        element: (count if element != template[-1] else count + 1) for element, count in count_elements_except_last(pairs_after_step(40, template, patterns)).items()})

print(f"Part2: {part2()}")
