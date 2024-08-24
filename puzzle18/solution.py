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

def get_possible_expansions(map, coords):
    adjacent_tiles = get_adjacent_coords(coords)
    adjacent_tiles = [coord for coord in adjacent_tiles if get_tile(map, coord) == "."]
    return adjacent_tiles

def solve_pt1(start_pos, grid_square_size):
    ans = 0
    pos = start_pos
    tile_map = ["."*grid_square_size for _ in range(grid_square_size)]
    for line in lines:
        direction = line[0]
        n_squares = line[1]
        for _ in range(n_squares):
            pos = go_direction(pos, direction)
            set_coord(tile_map, pos, "#")
    expansions = [(0, 0)]
    while len(expansions) > 0:
        coord = expansions[0]
        del expansions[0]
        set_coord(tile_map, coord, "O")
        new_expansion = get_possible_expansions(tile_map, coord)
        for tile in new_expansion:
            set_coord(tile_map, tile, "O")
        expansions = expansions + new_expansion
    for line in tile_map:
        ans += line.count("#")
        ans += line.count(".")
    return ans

def area_from_vertices(vertices):
    #WIP
    area = 0
    x_positions = sorted(list(set(vertex[0] for vertex in vertices)))
    return area

def solve_pt2():
    v1 = (0, 0)
    vertices = [v1]
    sides = []
    for instr in lines:
        direction = instr[0]
        distance = instr[1]
        direction_vector = multiply_coord(go_direction((0,0), direction), distance)
        new_vertex = add_coords(vertices[-1], direction_vector)
        vertices.append(new_vertex)
    return area_from_vertices(vertices)



#grid_square_size = 800
#pos =  (int(grid_square_size/2), int(grid_square_size/2))
#print("Part 1:", solve_pt1(pos, grid_square_size))
print("Part 2:", solve_pt2())