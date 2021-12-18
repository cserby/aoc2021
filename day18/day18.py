import math


def parse_input(file = "day18/sample"):
    with open(file) as input:
        return [ parse_snailfish_num(line.strip()) for line in input.readlines() ]

def parse_snailfish_num(str: str):
    return eval(str.replace("[", "(").replace("]", ")"))

def flatten_snailfish_num(sn):
    try:
        (left, right) = sn
        (left, right) = (flatten_snailfish_num(left), flatten_snailfish_num(right))
        while True:
            try:
                (left, right) = explode((left, right))
            except NothingToExplodeException:
                try:
                    (left, right) = split((left, right))
                except NothingToSplitException:
                    return (left, right)
    except TypeError:
        # Not a pair, but a single number
        return sn

class NothingToSplitException(Exception):
    pass

def split(sn):
    try:
        (left, right) = sn
        try:
            left = split(left)
        except NothingToSplitException:
            right = split(right)
        return (left, right)
    except TypeError:
        # Not a pair, but a single number
        if sn >= 10:
            return (math.floor(sn / 2), math.ceil(sn / 2))
        else:
            raise NothingToSplitException(sn)

class NothingToExplodeException(Exception):
    pass

def add_carry_to_the_rightmost(sn, carry):
    if carry == 0:
        return sn
    try:
        (left, right) = sn
        return (left, add_carry_to_the_rightmost(right, carry))
    except TypeError:
        # Not a pair, but a single number
        return sn + carry

def add_carry_to_the_leftmost(sn, carry):
    if carry == 0:
        return sn
    try:
        (left, right) = sn
        return (add_carry_to_the_leftmost(left, carry), right)
    except TypeError:
        # Not a pair, but a single number
        return sn + carry

def explode(sn):
    def __explode(sn):
        dpth = depth(sn)
        if dpth <= 4:
            raise NothingToExplodeException(sn)
        elif dpth == 5:
            return explode_N(sn)
        else:
            (left, right) = sn
            try:
                carry_left, result, carry_right = __explode(left)
                return carry_left, (result, add_carry_to_the_leftmost(right, carry_right)), 0
            except NothingToExplodeException:
                try:
                    carry_left, result, carry_right = __explode(right)
                    return 0, (add_carry_to_the_rightmost(left, carry_left), result), carry_right
                except NothingToExplodeException:
                    raise

    _, result, _ = __explode(sn)
    return result

def explode_N(sn):
    (left, right) = sn
    if depth(sn) == 1:
        return left, 0, right
    elif depth(left) >= depth(right):
        carry_left, result, carry_right = explode_N(left)
        return carry_left, (result, add_carry_to_the_leftmost(right, carry_right)), 0
    else:
        carry_left, result, carry_right = explode_N(right)
        return 0, (add_carry_to_the_rightmost(left, carry_left), result), carry_right

def depth(sn):
    try:
        (left, right) = sn
        return max(depth(left), depth(right)) + 1
    except TypeError:
        # Not a pair, but a single number
        return 0

def add_snailfish_num(sn1, sn2):
    return flatten_snailfish_num((sn1, sn2))

def sum_snailfish_num(sns):
    result = None
    for sn in sns:
        if result is None:
            result = sn
            continue
        result = add_snailfish_num(result, sn)
    return result

def magnitude(sn):
    if depth(sn) == 0:
        return sn
    (left, right) = sn
    if depth(sn) == 1:
        return 3*left + 2*right
    else:
        return 3*magnitude(left) + 2*magnitude(right)

def part1():
    return magnitude(sum_snailfish_num(parse_input("day18/input")))

print(f"Part1: {part1()}")