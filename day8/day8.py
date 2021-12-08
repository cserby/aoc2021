def parse_input():
    with open("day8/input") as input:
        return [([frozenset(pattern) for pattern in patterns.split()],
            [ frozenset(digit) for digit in digits.split() ]) for patterns, digits in [ line.strip().split("|") for line in input.readlines() ]]

def part1():
    displays = parse_input()
    count = 0
    for (_, digits) in displays:
        for digit in digits:
            l = len(digit)
            if l == 2 or l == 3 or l == 4 or l == 7:
                count += 1
    return count

def part2():
    def map_digits(pattern: list[frozenset], digits: list[str]):
        mapping: dict[int, frozenset] = {
            "1": next(iter(p for p in pattern if len(p) == 2)),
            "4": next(iter(p for p in pattern if len(p) == 4)),
            "7": next(iter(p for p in pattern if len(p) == 3)),
            "8": next(iter(p for p in pattern if len(p) == 7)),
        }
        mapping.update({
            "9": [p for p in pattern if len(p) == 6 and len(p ^ (mapping["4"] | mapping["7"])) == 1][0]
        })
        mapping.update({
            "0": [p for p in pattern if len(p) == 6 and p != mapping["9"] and len(p ^ mapping["7"]) == 3][0]
        })
        mapping.update({
            "6": [p for p in pattern if len(p) == 6 and p != mapping["9"] and p != mapping["0"]][0]
        })
        mapping.update({
            "3": [p for p in pattern if len(p) == 5 and len(p ^ mapping["7"]) == 2][0]
        })
        mapping.update({
            "5": [p for p in pattern if len(p) == 5 and p != mapping["3"] and len(p ^ mapping["9"]) == 1][0]
        })
        mapping.update({
            "2": [p for p in pattern if len(p) == 5 and p != mapping["3"] and p != mapping["5"]][0]
        })
        inv_mapping = { v: k for k, v in mapping.items() }
        return int("".join([inv_mapping[digit] for digit in digits]))


    displays = parse_input()
    return sum(map_digits(pattern, digits) for (pattern, digits) in displays)

print(f"Part1: {part1()}")
print(f"Part2: {part2()}")
