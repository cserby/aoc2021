A = 1
B = 10
C = 100
D = 1000

def part1():
    return 3*A + 3*A + 4*C + 5*B + 7*C + 6*B + 5*A + 6*D + 5*D + 3*C + 9*A

if __name__ == "__main__":
    print(f"Part1: {part1()}")