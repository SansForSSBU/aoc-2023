import math

lines = []
with open("puzzle5/input.txt") as input:
    lines = input.read().split("\n")

seeds = [int(x) for x in lines[0].split(" ")[1:]]
maps = []
map = []
for line in lines[2:]:
    if line == "":
        maps.append(map)
        map = []
    elif line[0].isalpha():
        continue
    else:
        map.append([int(x) for x in line.split(" ")])

maps.append(map)

def can_use(mapping, num):
    if num >= mapping[1] and num <= mapping[1] + mapping[2] - 1:
        return True
    return False

def translate(mapping, num):
    return num + (mapping[0] - mapping[1])

def find_all_endpoints(seed, almanac):
    if len(almanac) == 0:
        return [seed]
    mapping = almanac[0]
    valid_mappings = [m for m in mapping if can_use(m, seed)]
    valid_next_seeds = [translate(m, seed) for m in valid_mappings]
    ends = []
    if len(valid_next_seeds) == 0:
        ends = ends + find_all_endpoints(seed, almanac[1:])
    for s in valid_next_seeds:
        ends = ends + find_all_endpoints(s, almanac[1:])
    return ends

def solve_pt1():
    lowest = math.inf
    for seed in seeds:
        lowest = min(min(find_all_endpoints(seed, maps)), lowest)
    return lowest

def solve_pt2():
    return 0

print(solve_pt1())
print(solve_pt2())