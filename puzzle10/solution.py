from enum import Enum

lines = []
with open("puzzle10/input.txt") as input:
    lines = input.read().split("\n")

start_coords = ()
for y, line in enumerate(lines):
    if "S" in line:
        x = line.find("S")
        start_coords = (x, y)
        lines[y] = line.replace("S","F")
        break

class D(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

inverse_dirs = {
    D.NORTH: D.SOUTH,
    D.EAST: D.WEST,
    D.SOUTH: D.NORTH,
    D.WEST: D.EAST
}

mappings = {
    "|": (D.NORTH, D.SOUTH),
    "-": (D.WEST, D.EAST),
    "L": (D.NORTH, D.EAST),
    "J": (D.NORTH, D.WEST),
    "7": (D.SOUTH, D.WEST),
    "F": (D.SOUTH, D.EAST),
    ".": ()
}
def go_direction(pos, direction):
    if direction == D.NORTH:
        return (pos[0], pos[1] - 1)
    elif direction == D.EAST:
        return (pos[0] + 1, pos[1])
    elif direction == D.SOUTH:
        return (pos[0], pos[1] + 1)
    elif direction == D.WEST:
        return (pos[0] - 1, pos[1])

def get_tile(coords):#(x, y)
    if coords[0] < 0 or coords[0] >= len(lines[0]) or coords[1] < 0 or coords[1] >= len(lines[1]):
        return None
    return lines[coords[1]][coords[0]]

def solve_pt1():
    start_directions = mappings[get_tile(start_coords)]
    loc1_dir = start_directions[0]
    loc2_dir = start_directions[1]
    loc1 = start_coords
    loc2 = start_coords
    steps = 0
    while (loc1 != loc2) or steps == 0:
        steps += 1
        loc1 = go_direction(loc1, loc1_dir)
        loc1_dir = [x for x in mappings[get_tile(loc1)] if x != inverse_dirs[loc1_dir]][0]

        loc2 = go_direction(loc2, loc2_dir)
        loc2_dir = [x for x in mappings[get_tile(loc2)] if x != inverse_dirs[loc2_dir]][0]

    return steps

def get_adjacent_coords(coords):
    adjacent_coords = [
        (coords[0], coords[1] + 1),
        (coords[0], coords[1] - 1),
        (coords[0] + 1, coords[1]),
        (coords[0] - 1, coords[1]),
    ]
    return adjacent_coords

def get_possible_expansions(coords):
    adjacent_tiles = get_adjacent_coords(coords)
    adjacent_tiles = [coord for coord in adjacent_tiles if get_tile(coord) == "."]
    return adjacent_tiles

def get_blocked_subpixels(border_square):
    mid = get_middle_subpixel(border_square)
    directions = mappings[get_tile(border_square)]
    blocked_subpixels = [mid]
    for direction in directions:
        blocked_subpixels.append(go_direction(mid, direction))
    return blocked_subpixels

def get_middle_subpixel(full_pixel):
    return ((full_pixel[0]*3) + 1, (full_pixel[1] * 3) + 1)

def get_full_pixel(subpixel):
    return (int(subpixel[0]/3), int(subpixel[0]/3))

def set_pixel(coords, char):
    line = lines[coords[1]]
    list1 = list(line)
    list1[coords[0]] = char
    newline=''.join(list1)
    lines[coords[1]] = newline

def print_map():
    for line in lines:
        print(line)

def solve_pt2():
    loop_coords = []
    start_directions = mappings[get_tile(start_coords)]
    loc1_dir = start_directions[0]
    loc1 = start_coords
    steps = 0
    while (loc1 != start_coords) or steps == 0:
        loop_coords.append((loc1))
        steps += 1
        loc1 = go_direction(loc1, loc1_dir)
        loc1_dir = [x for x in mappings[get_tile(loc1)] if x != inverse_dirs[loc1_dir]][0]
    print(len(loop_coords))
    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            if (x, y) not in loop_coords:
                set_pixel((x, y), ".")
    del loop_coords
    print("Finished map setup")
    expansions = [(0, 0)]
    while len(expansions) > 0:
        coord = expansions[0]
        del expansions[0]
        set_pixel(coord, "O")
        new_expansion = get_possible_expansions(coord)
        for tile in new_expansion:
            set_pixel(tile, "O")
        expansions = expansions + new_expansion

    print_map()

    

    #print_map()
    return 0
    # Now comes the fun part

print(solve_pt1())
print(get_tile((10, 10)))
print(get_blocked_subpixels((10, 10)))
print(solve_pt2())