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

def put_in_range(seed_range, mapping):
    used_tiles = None
    new_mapping = None
    if seed_range[0] in range(mapping[1], mapping[1] + mapping[2]):
        # Start of seed range is in plot range
        lost_squares =  seed_range[0] - mapping[1]
        translation = (mapping[0]-mapping[1])
        used_tiles = [seed_range[0], min(mapping[2]-lost_squares, seed_range[1])]
        new_mapping = [used_tiles[0]+translation, used_tiles[1]]
    elif mapping[1] in range(seed_range[0], seed_range[0] + seed_range[1] + 1):
        # Start of plot range is in seed range
        lost_squares =   mapping[1] - seed_range[0]
        translation = (mapping[0]-mapping[1])
        used_tiles = [mapping[1], min(seed_range[1]-lost_squares, mapping[2])]
        new_mapping = [used_tiles[0]+translation, used_tiles[1]]
    return used_tiles,new_mapping

def find_next_seed_ranges(seed_range, mappings):
    used_tile_ranges = []
    next_ranges = []
    for mapping in mappings:
        used_tiles,new_range = put_in_range(seed_range, mapping)
        if new_range:
            next_ranges.append(new_range)
            used_tile_ranges.append(used_tiles)
    return used_tile_ranges,next_ranges

def find_all_range_endpoints(seed_range, almanac):
    if len(almanac) == 0:
        return [seed_range]
    used_tile_ranges,next_ranges = find_next_seed_ranges(seed_range, almanac[0])
    all_next_ranges = []
    for next_range in next_ranges:
        all_next_ranges = all_next_ranges + find_all_range_endpoints(next_range, almanac[1:])
    return all_next_ranges

def solve_pt1():
    lowest = math.inf
    for seed in seeds:
        lowest = min(min(find_all_endpoints(seed, maps)), lowest)
    return lowest

def solve_pt2():
    seed_ranges = []
    i = 0
    while i <= len(seeds) - 2:
        seed_ranges.append([seeds[i], seeds[i+1]])
        i+=2
    best = math.inf
    for seed_range in seed_ranges:
        result = find_all_range_endpoints(seed_range, maps)
        if len(result) > 0:
            best = min(min([ra[0] for ra in result]), best)
    return best

print(solve_pt1())
print(solve_pt2())