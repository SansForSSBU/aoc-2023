lines = []
with open("puzzle14/input.txt") as input:
    lines = input.read().split("\n")

def print_map(map):
    for line in map:
        print(line)

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def find_next_y(map, coord):
    if coord[1] > 30:
        pass
    l = get_column(map, coord[0])
    y = max(l.rfind("O", 0, coord[1]), l.rfind("#", 0, coord[1])) + 1
    return y

def set_coord(map, coord, char):
    map[coord[1]] = map[coord[1]][:coord[0]] + char + map[coord[1]][coord[0]+1:]

def solve_pt1():
    load = 0
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                new_y = find_next_y(lines, (x, y))
                set_coord(lines, (x, y), ".")
                set_coord(lines, (x, new_y), "O")
                load += len(lines) - new_y
    return load
def solve_pt2():
    return 0

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())