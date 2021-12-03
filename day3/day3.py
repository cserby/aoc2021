input = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''.splitlines()

def read_instructions():
    with open("day3/input") as input:
        return input.readlines()

input = read_instructions()

def parse_input(lst):
    parsed = list(zip(*[ list(line) for line in lst ]))
    return parsed

def most_commons(parsed, prefer="0"):
    return [ most_common(pos, prefer=prefer) for pos in parsed ]

def least_commons(parsed, prefer="0"):
    return [ least_common(pos, prefer=prefer) for pos in parsed ]

def gamma_rate(parsed):
    gamma_rate = bin_to_dec(most_commons(parsed))
    return gamma_rate

def most_common(st, prefer):
    count_1 = len([ item for item in st if item == "1" ])
    half = len(st) / 2
    if count_1 > half:
        return "1"
    elif count_1 == half:
        return prefer
    else:
        return "0"

def least_common(st, prefer):
    count_1 = len([ item for item in st if item == "1" ])
    half = len(st) / 2
    if count_1 < half:
        return "1"
    elif count_1 == half:
        return prefer
    else:
        return "0"

def bin_to_dec(lst):
    return int("".join(lst), 2)

def epsilon_rate(parsed):
    epsilon_rate = bin_to_dec(least_commons(parsed))
    return epsilon_rate

def oxygen_rate():
    filtered = input
    for index in range(len(filtered[0])):
        mcs = most_commons(parse_input(filtered), prefer="1")
        filtered = [ item for item in filtered if item[index] == mcs[index]]
        if len(filtered) <= 1:
            break
    assert len(filtered) == 1
    return bin_to_dec(filtered[0])

def co2_scrubber_rate():
    filtered = input
    for index in range(len(filtered[0])):
        mcs = least_commons(parse_input(filtered), prefer="0")
        print(f"Filtered: {filtered} mcs: {mcs}")
        filtered = [ item for item in filtered if item[index] == mcs[index]]
        print(f"New filtered: {filtered}")
        if len(filtered) <= 1:
            break
    assert len(filtered) == 1
    return bin_to_dec(filtered[0])

parsed = parse_input(input)

g_r = gamma_rate(parsed)
e_r = epsilon_rate(parsed)

print(f"Part1: {g_r * e_r}")

o_r = oxygen_rate()
c_r = co2_scrubber_rate()

print(f"Part2: {o_r * c_r}")