import functools

def read_measurements():
    with open("day1/input") as input:
        return [ int(line) for line in input.readlines()]

measurements = read_measurements()

def count_increases(lst):
    def reduce_fn(prev, curr):
        (prev_head, increases) = prev
        return (curr, increases + 1 if prev_head is not None and curr > prev_head else increases)

    (_, increases) = functools.reduce(reduce_fn, lst, (None, 0))
    return increases



def part1():
    return count_increases(measurements)

def part2():
    def sliding_windows_of_3(list):
        for index in range(0, len(list)):
            yield list[index : index + 3]

    return count_increases([ sum(sw) for sw in sliding_windows_of_3(measurements)])

print(f"Part1: {part1()}")
print(f"Part2: {part2()}")