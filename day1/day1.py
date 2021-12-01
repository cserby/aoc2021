prev_depth = None
depth_increased = 0

with open("day1/input") as input:
    for line in input:
        curr_depth = int(line)
        if prev_depth is not None and curr_depth > prev_depth:
            depth_increased += 1
        prev_depth = curr_depth

print(depth_increased)