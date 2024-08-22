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
    return lines[coords[1]][coords[0]]

def solve_pt1():
    start_directions = mappings[get_tile(start_coords)]
    print(start_directions)
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

def solve_pt2():
    return 0

print(solve_pt1())
print(solve_pt2())