from enum import Enum
import heapq

lines = []
with open("puzzle18/input.txt") as input:
    lines = input.read().split("\n")

class D(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

conversion = {
    "U": D.NORTH,
    "R": D.EAST,
    "D": D.SOUTH,
    "L": D.WEST
}

lines = [line.split(" ") for line in lines]
for line in lines:
    line[0] = conversion[line[0]]
    line[1] = int(line[1])

def go_direction(pos, direction):
    if direction == D.NORTH:
        return (pos[0], pos[1] - 1)
    elif direction == D.EAST:
        return (pos[0] + 1, pos[1])
    elif direction == D.SOUTH:
        return (pos[0], pos[1] + 1)
    elif direction == D.WEST:
        return (pos[0] - 1, pos[1])

def get_adjacent_coords(coords):
    adjacent_coords = [
        (coords[0], coords[1] + 1),
        (coords[0], coords[1] - 1),
        (coords[0] + 1, coords[1]),
        (coords[0] - 1, coords[1]),
    ]
    return adjacent_coords

def print_map(map):
    for line in map:
        print(line)

def get_tile(grid, coords):
    if coords[0] < 0 or coords[0] >= len(grid[0]) or coords[1] < 0 or coords[1] >= len(grid[1]):
        return None
    return grid[coords[1]][coords[0]]

def set_coord(map, coord, char):
    map[coord[1]] = map[coord[1]][:coord[0]] + char + map[coord[1]][coord[0]+1:]

def add_coords(coord1, coord2):
    return (coord1[0]+coord2[0], coord1[1]+coord2[1])

def sub_coords(coord1, coord2):
    return (coord1[0]-coord2[0], coord1[1]-coord2[1])

def multiply_coord(coord, factor):
    return (coord[0]*factor, coord[1]*factor)

def unit_vector(vector):
    x = 0
    y = 0
    if vector[0] < 0: x = -1
    if vector[0] > 0: x = 1
    if vector[1] < 0: y = -1
    if vector[1] > 0: y = 1
    return (x, y)

# Formula from https://tinyurl.com/yvyz9bd9
def area_from_vertices(vertices):
    area = 0
    n_vertices = len(vertices)
    for i in range(len(vertices) - 1):
        x_n = vertices[i][0]
        y_n = vertices[i][1]
        x_np1 = vertices[i+1][0]
        y_np1 = vertices[i+1][1]
        term = 0.5*(x_n*y_np1 - x_np1*y_n)
        area += term
    return area

def solve_pt1():
    perimeter = 0
    v1 = (0, 0)
    vertices = [v1]
    sides = []
    for instr in lines:
        direction = instr[0]
        distance = instr[1]
        direction_vector = multiply_coord(go_direction((0,0), direction), distance)
        new_vertex = add_coords(vertices[-1], direction_vector)

        vertices.append(new_vertex)
        perimeter += distance
    return int(area_from_vertices(vertices) + perimeter/2 + 1)

print("Part 1:", solve_pt1())
translation = {
    0: D.EAST,
    1: D.SOUTH,
    2: D.WEST,
    3: D.NORTH
}
for line in lines:
    color = line[2]
    color = color.strip("()#")
    line[0] = translation[int(color[-1])]
    line[1] = int(color[:-1], 16)
    
print("Part 2:", solve_pt1())