from enum import Enum
lines = []
with open("puzzle14/input.txt") as input:
    lines = input.read().split("\n")

class D(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def print_map(map):
    for line in map:
        print(line)

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def find_next_pos(map, coord, dir):
    x = coord[0]
    y = coord[1]
    if dir == D.NORTH:
        l = get_column(map, coord[0])
        y = max(l.rfind("O", 0, coord[1]), l.rfind("#", 0, coord[1])) + 1
    return (x, y)

def set_coord(map, coord, char):
    map[coord[1]] = map[coord[1]][:coord[0]] + char + map[coord[1]][coord[0]+1:]

def move_rock(map, coord, dir):
    x = coord[0]
    y = coord[1]
    set_coord(map, (x, y), ".")
    next_pos = find_next_pos(map, coord, dir)
    set_coord(map, next_pos, "O")
    return next_pos

def solve_pt1():
    load = 0
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                new_pos = move_rock(lines, (x, y), D.NORTH)
                load += len(lines) - new_pos[1]
    return load
def solve_pt2():
    return 0

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())