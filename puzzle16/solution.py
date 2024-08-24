from enum import Enum

lines = []
with open("puzzle16/input.txt") as input:
    lines = input.read().split("\n")

class D(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

mappings = {
    ".": {},
    "/": {
        D.NORTH: [D.EAST],
        D.EAST: [D.NORTH],
        D.SOUTH: [D.WEST],
        D.WEST: [D.SOUTH]
    },
    "\\": {
        D.NORTH: [D.WEST],
        D.EAST: [D.SOUTH],
        D.SOUTH: [D.EAST],
        D.WEST: [D.NORTH]
    },
    "|": {
        D.EAST: [D.NORTH, D.SOUTH],
        D.WEST: [D.NORTH, D.SOUTH]
        },
    "-": {
        D.NORTH: [D.EAST, D.WEST],
        D.SOUTH: [D.EAST, D.WEST]
    }
}

def get_tile(map, coords):
    if coords[0] < 0 or coords[0] >= len(map[0]) or coords[1] < 0 or coords[1] >= len(map[1]):
        return None
    return map[coords[1]][coords[0]]

def go_direction(pos, direction):
    if direction == D.NORTH:
        return (pos[0], pos[1] - 1)
    elif direction == D.EAST:
        return (pos[0] + 1, pos[1])
    elif direction == D.SOUTH:
        return (pos[0], pos[1] + 1)
    elif direction == D.WEST:
        return (pos[0] - 1, pos[1])

def get_new_directions(beam, grid):
    coords = beam[0]
    direction = beam[1]
    tile = get_tile(grid, coords)
    new_directions = mappings[tile].get(direction, [direction]) # If unmapped, keep going curr direction
    return new_directions

def coords_in_grid(coord, grid):
    return coord[0] in range(len(grid[0])) and coord[1] in range(len(grid))

energised_squares = {}
def simulate_beam(beam, grid):
    coords = beam[0]
    direction = beam[1]
    square_prev_beams = energised_squares.get(coords, [])
    if direction in square_prev_beams:
        return [] # We've on the same path as a previous beam, so stop.
    energised_squares[coords] = square_prev_beams + [direction]
    # Should we also add new directions?
    new_directions = get_new_directions(beam, grid)
    new_beams = []
    for direction in new_directions:
        next_coords = go_direction(coords, direction)
        if coords_in_grid(next_coords, grid):
            new_beams.append([next_coords, direction])
    return new_beams


def solve_pt1():
    starting_beam = [(0, 0), D.EAST]
    beams = [starting_beam]
    while len(beams) > 0:
        beam = beams[0]
        del beams[0]
        beams = beams + simulate_beam(beam, lines)
        pass
    return len(energised_squares.keys())
def solve_pt2():
    return 0

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())