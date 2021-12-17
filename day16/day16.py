from functools import reduce
from itertools import islice, tee, zip_longest
from operator import mul


def parse_input():
    with open("day16/input") as input:
        return input.readline().strip()

def hex_to_bin_str(str):
    bin_str = ""
    for hex_digit in str:
        bin_str += f"{int(hex_digit, 16):0>4b}"
    return bin_str

def chunks(iterable, chunk_size):
    args = [iter(iterable)] * chunk_size
    for chunk in zip_longest(*args, fillvalue="0"):
        yield "".join(chunk)

def take(iterable, n):
    return "".join(islice(iterable, n))

def consume(iterable):
    [ _ for _ in iterable ]

def parse_operator(iterable, version, type_field):
    length_type_id = take(iterable, 1)
    if length_type_id == '0':
        total_length_in_bits = int(take(iterable, 15), 2)
        sub_packets = [ sub_packet for sub_packet in parse_all(take(iterable, total_length_in_bits)) ]
    if length_type_id == '1':
        number_of_subpackets = int(take(iterable, 11), 2)
        sub_packets = [ sub_packet for sub_packet in parse_n(iterable, number_of_subpackets)]
    return {
        "version": int(version, 2),
        "type_field": int(type_field, 2),
        "sub_packets": sub_packets,
    }

def parse_literal(iterable, version):
    literal = ""
    for chunk in chunks(iterable, 5):
        literal += chunk[1:]
        if chunk[0] == "0":
            break
    return {
        "version": int(version, 2),
        "type_field": int("100", 2),
        "value": int(literal, 2)
    }

def has_elements(iterable):
  iterable, copy = tee(iterable)
  return any(True for _ in copy), iterable

def parse_n(str, n):
    iterable = (bit for bit in str)

    for _ in range(n):
        version = take(iterable, 3)
        type_field = take(iterable, 3)
        if type_field == "100":
            yield parse_literal(iterable, version)
        else:
            yield parse_operator(iterable, version, type_field)

def parse_all(str):
    iterable = (bit for bit in str)

    while True:
        has_more, iterable = has_elements(iterable)
        if not has_more:
            break

        version = take(iterable, 3)
        type_field = take(iterable, 3)
        if type_field == "100":
            yield parse_literal(iterable, version)
        else:
            yield parse_operator(iterable, version, type_field)

def parse_one(str):
    iterable = (bit for bit in str)

    version = take(iterable, 3)
    type_field = take(iterable, 3)
    if type_field == "100":
        literal = parse_literal(iterable, version)
        consume(iterable)
        return literal
    else:
        operator = parse_operator(iterable, version, type_field)
        consume(iterable)
        return operator

def version_numbers(packet):
    if "sub_packets" in packet.keys():
        for sub_packet in packet["sub_packets"]:
            yield from version_numbers(sub_packet)
    yield packet["version"]

def sum_of_version_numbers(packet):
    return sum(vn for vn in version_numbers(packet))

def part1():
    return sum(version_numbers(parse_one(hex_to_bin_str(parse_input()))))

print(f"Part1: {part1()}")

def evaluate(packet):
    if packet["type_field"] == 4:
        return packet["value"]
    elif packet["type_field"] == 0:
        return sum(evaluate(packet) for packet in packet["sub_packets"])
    elif packet["type_field"] == 1:
        return reduce(mul, (evaluate(packet) for packet in packet["sub_packets"]), 1)
    elif packet["type_field"] == 2:
        return min(evaluate(packet) for packet in packet["sub_packets"])
    elif packet["type_field"] == 3:
        return max(evaluate(packet) for packet in packet["sub_packets"])
    elif packet["type_field"] == 5: #gt
        return 1 if evaluate(packet["sub_packets"][0]) > evaluate(packet["sub_packets"][1]) else 0
    elif packet["type_field"] == 6: #lt
        return 1 if evaluate(packet["sub_packets"][0]) < evaluate(packet["sub_packets"][1]) else 0
    elif packet["type_field"] == 7: #eq
        return 1 if evaluate(packet["sub_packets"][0]) == evaluate(packet["sub_packets"][1]) else 0

def part2(str = parse_input()):
    return evaluate(parse_one(hex_to_bin_str(str)))

print(f"Part2: {part2()}")
