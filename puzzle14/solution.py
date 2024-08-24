from enum import Enum
from math import floor

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

def get_line(map, y):
    return map[y]

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def find_next_pos(map, coord, dir):
    # South may not be working. Fix later.
    x = coord[0]
    y = coord[1]
    if y == 50:
        pass
    if dir == D.NORTH:
        l = get_column(map, coord[0])
        y = max(l.rfind("O", 0, coord[1]), l.rfind("#", 0, coord[1])) + 1

    elif dir == D.EAST:
        l = get_line(map, y)
        next_rock = l.find("O", coord[0])
        if next_rock == -1: next_rock = len(l)
        next_hash = l.find("#", coord[0])
        if next_hash == -1: next_hash = len(l)
        x = min(next_rock,next_hash)-1
    
    elif dir == D.SOUTH:
        l = get_column(map, coord[0])
        next_rock = l.find("O", coord[1])
        if next_rock == -1: next_rock = len(l)
        next_hash = l.find("#", coord[1])
        if next_hash == -1: next_hash = len(l)
        y = min(next_rock,next_hash)-1
    
    elif dir == D.WEST:
        l = get_line(map, y)
        x = max(l.rfind("O", 0, coord[0]), l.rfind("#", 0, coord[0])) + 1

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

def get_load(map):
    load = 0
    for y, l in enumerate(map):
        for x, c in enumerate(l):
            if c == "O":
                load += len(map) - y
    return load

def solve_pt1():
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                new_pos = move_rock(lines, (x, y), D.NORTH)
    return get_load(lines)

def spin_cycle():
    # North
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                move_rock(lines, (x, y), D.NORTH)

    # West
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                move_rock(lines, (x, y), D.WEST)

    # South
    for y, l in reversed(list(enumerate(lines))):
        for x, c in enumerate(l):
            if c == "O":
                move_rock(lines, (x, y), D.SOUTH)

    # East
    for y, l in enumerate(lines):
        for x, c in reversed(list(enumerate(l))):
            if c == "O":
                move_rock(lines, (x, y), D.EAST)
    
    
    return 0

def hash_map(map):
    return hash(tuple(map))

def solve_pt2(n_cycles):
    hashes = {}
    n = 0
    have_skipped = False
    while n < n_cycles:
        spin_cycle()
        n += 1
        pos_hash = hash_map(lines)
        if hashes.get(pos_hash) and not have_skipped:
            cycle_len = n - hashes[pos_hash]
            n_skips = floor((n_cycles - n) / cycle_len)
            n += cycle_len * n_skips # nyooooooom
            have_skipped = True
        else:
            hashes[pos_hash] = n
    return get_load(lines)


lines_backup = lines.copy()
print("Part 1:", solve_pt1())
lines = lines_backup.copy()
print("Part 2:", solve_pt2(1000000000))