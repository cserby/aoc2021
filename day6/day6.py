def parse_input():
    with open("day6/input") as input:
        return [ int(i) for i in input.readline().split(",") ]

day0_pop = parse_input()

def day0_pop_increment_on_day(day):
    return sum(1 for lanterfish in day0_pop if lanterfish == day % 7)

daily_increments = {}

def calculate_daily_increment(day):
    inc = day0_pop_increment_on_day(day)

    inc += daily_increment(day - 9)
    i = day - 9 - 7
    while i > 0:
        inc += daily_increment(i)
        i -= 7
    return inc

def daily_increment(day):
    if day < 0:
        return 0
    try:
        return daily_increments[day]
    except KeyError:
        daily_increments[day] = calculate_daily_increment(day)
        return daily_increments[day]

pop = len(day0_pop)
for day in range(80):
    pop += daily_increment(day)
    print(f"Day{day+1}: {daily_increment(day)}, population: {pop}")

print(f"Part1: {pop}")