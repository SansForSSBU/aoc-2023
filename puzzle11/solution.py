
lines = []
with open("puzzle11/input.txt") as input:
    lines = input.read().split("\n")

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def is_empty(line):
    return line.count(".") == len(line)

def get_empty_lines(map):
    empty_lines = []
    for y, line in enumerate(map):
        if is_empty(line):
            empty_lines.append(y)

    empty_columns = []
    empty_column_example = ""
    for x in range(len(map[0])-1, -1, -1):
        column = get_column(map, x)
        if is_empty(column):
            empty_columns.append(x)
    
    return empty_lines,empty_columns

def get_galaxy_coords(map):
    coords = []
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "#":
                coords.append((x, y))
    return coords

def taxicab_distance_part2(point1, point2, empty_rows, empty_columns, factor):
    result = abs(point1[0]-point2[0]) + abs(point1[1] - point2[1])
    x_crossed = range(min(point1[0], point2[0]), max(point1[0], point2[0]))
    y_crossed = range(min(point1[1], point2[1]), max(point1[1], point2[1]))
    for x in empty_columns:
        if x in x_crossed:
            result += (factor-1)
    for y in empty_rows:
        if y in y_crossed:
            result += (factor-1)
    return result

def solve_pt1(factor):
    empty_rows, empty_columns = get_empty_lines(lines)
    galaxy_coords = get_galaxy_coords(lines)
    result = 0
    for n, point1 in enumerate(galaxy_coords):
        for point2 in galaxy_coords[n+1:]:
            result += taxicab_distance_part2(point1, point2, empty_rows, empty_columns, factor)
    return result

print("Part 1:", solve_pt1(2))
print("Part 2:", solve_pt1(1000000))
