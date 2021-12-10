from functools import reduce

def parse_input():
    with open("day10/input") as input:
        return [[ char for char in list(line.strip())] for line in input.readlines() ]

def invert_bracket(char):
    if char == '(':
        return ')'
    elif char == '[':
        return ']'
    elif char == '{':
        return '}'
    elif char == '<':
        return '>'
    else:
        raise Exception(char)

def part1():
    values = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    def get_first_incorrect_char(line):
        stack = []

        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                stack = stack + [ char ]
            elif char == ')' or char == ']' or char == '}' or char == '>':
                try:
                    top = stack.pop()
                except IndexError:
                    return char
                if char == invert_bracket(top):
                    continue
                else:
                    return char

    lines = parse_input()
    return sum([ values[char] for char in [ get_first_incorrect_char(line) for line in lines ] if char is not None ])

print(part1())

def part2():

    scores = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def get_completion(line):
        stack = []

        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                stack = stack + [ char ]
            elif char == ')' or char == ']' or char == '}' or char == '>':
                try:
                    top = stack.pop()
                except IndexError:
                    return None
                if char == invert_bracket(top):
                    continue
                else:
                    return None
        return reduce(lambda prev, curr: prev*5 + curr, reversed([ scores[invert_bracket(char)] for char in stack ]), 0)

    lines = parse_input()
    line_scores = sorted([ completion for completion in [ get_completion(line) for line in lines ] if completion is not None])
    return line_scores[int(len(line_scores) / 2)]

print(part2())