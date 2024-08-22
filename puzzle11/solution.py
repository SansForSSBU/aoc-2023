
lines = []
with open("puzzle11/input.txt") as input:
    lines = input.read().split("\n")

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def is_empty(line):
    return line.count(".") == len(line)

def insert_column(map, pos, column):
    for i, line in enumerate(map):
        new_line = line[:pos] + column[i] + line[pos:]
        map[i] = new_line

def expand_empty_lines(map):
    empty_lines = []
    empty_line_example = ""
    for y, line in enumerate(map):
        if is_empty(line):
            empty_lines.append(y)
            empty_line_example = line
    for y in reversed(empty_lines):
        map.insert(y, empty_line_example)

    empty_columns = []
    empty_column_example = ""
    for x in range(len(map[0])-1, -1, -1):
        column = get_column(map, x)
        if is_empty(column):
            empty_columns.append(x)
            empty_column_example = column

    for x in empty_columns:
        insert_column(map, x, empty_column_example)

def get_galaxy_coords(map):
    coords = []
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "#":
                coords.append((x, y))
    return coords

def taxicab_distance(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1] - point2[1])

def print_map(map):
    for line in map:
        print(line)

def solve_pt1():

    print(len(get_galaxy_coords(lines)))
    expand_empty_lines(lines)
    galaxy_coords = get_galaxy_coords(lines)
    print(len(galaxy_coords))
    result = 0
    for n, point1 in enumerate(galaxy_coords):
        if n == len(galaxy_coords) - 2:
            print("Hello")
        for point2 in galaxy_coords[n+1:]:
            result += taxicab_distance(point1, point2)
    return result

def solve_pt2():
    return 0

print(solve_pt1())
print(solve_pt2())


