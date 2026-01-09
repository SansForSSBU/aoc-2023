import numpy as np
import math

class Grid():
    def __init__(self, grid):
        self.grid = grid

    def is_in_grid(self, pos):
        (x, y) = pos
        if x >= len(self.grid[0]) or x < 0:
            return False
        if y >= len(self.grid) or y < 0:
            return False
        return True
    
    def get_pu_offset(self, pos):
        if self.is_in_grid(pos):
            return (0,0)
        (x, y) = pos
        if x < 0:
            return (-1,0)
        if y < 0:
            return (0,-1)
        if x >= len(self.grid[0]):
            return (1,0)
        if y >= len(self.grid[1]):
            return (0,1)
        raise Exception()
    
    def snap_to_grid(self, pos):
        (x, y) = pos
        x = x % len(self.grid[0])
        y = y % len(self.grid)
        return (x,y)

    def get_coords(self, pos):
        (x, y) = pos
        if not self.is_in_grid(pos):
            return -1
        return self.grid[y][x]
    
    def set_coords(self, pos, val):
        (x, y) = pos
        if not self.is_in_grid(pos):
            return False
        self.grid[y][x] = val
    
    def get_adjacents(self, pos):
        (x, y) = pos
        adds = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for add in adds:
            extra_pos = (x + add[0], y + add[1])
            if self.is_in_grid(extra_pos) and not self.is_rock(extra_pos):
                yield extra_pos

    def is_rock(self, pos):
        return self.get_coords(pos) == 1

def add_positions(a,b):
    return (a[0]+b[0], a[1]+b[1])

def count_occ(grid):
    grid = Grid(grid)
    even_occupancy = 0
    odd_occupancy = 0
    for x in range(len(grid.grid[0])):
        for y in range(len(grid.grid)):
            if grid.get_coords((x,y)) == 1:
                if sum([x,y]) % 2 == 0:
                    even_occupancy += 1
                else:
                    odd_occupancy += 1
    return (even_occupancy, odd_occupancy)

def get_occupancy(grid, farmer_pos, n_steps):
    occupancy = Grid(np.zeros_like(grid.grid))
    occupancy.set_coords(farmer_pos, 1)
    to_check = [farmer_pos]
    for i in range(n_steps):
        next_to_check = set()
        for pos in to_check:
            for adj in grid.get_adjacents(pos):
                if grid.get_coords(adj) == 0:
                    next_to_check.add(adj)
                    occupancy.set_coords(adj, 1)
        to_check = list(next_to_check)

    (even_occupancy, odd_occupancy) = count_occ(occupancy.grid)
    return even_occupancy, odd_occupancy, occupancy

def solve_pt1(grid, farmer_pos, n_steps):
    (even_occupancy, odd_occupancy, _) = get_occupancy(grid, farmer_pos, n_steps)
    if (sum(farmer_pos)+n_steps) % 2 == 0:
        return even_occupancy
    else:
        return odd_occupancy

def n_grids(n_field_steps, occupancies, n_steps):
    n_field_steps = n_field_steps
    ans = 0
    even_fields = 1
    odd_fields = 0
    for n in range(1,n_field_steps):
        idx = (n+n_steps) % 2
        ans += 4 * n * occupancies["C"][idx]
    
    n = n_field_steps
    idx = (n+n_steps) % 2
    ans += occupancies["N"][idx] + occupancies["E"][idx] + occupancies["S"][idx] + occupancies["W"][idx]
    ans += (occupancies["NE"][idx] + occupancies["SE"][idx] + occupancies["SW"][idx] + occupancies["NW"][idx]) * (n-4)
    return ans
    #return 2*n_field_steps*n_field_steps + 2*n_field_steps + 1

def detile(tiled, n=3):
    h = tiled.shape[0] // n
    w = tiled.shape[1] // n
    return (
        tiled
        .reshape(n, h, n, w)
        .swapaxes(1, 2)
        .reshape(n*n, h, w)
    )

def swap(tup):
    return (tup[1], tup[0])

def solve_pt2(grid, farmer_pos, n_steps=26501365):
    # 637531791816968 too low
    # 637525510428520 too low
    # 637531813260100 too low
    # 637538093084305 wrong
    # First, just think about the spaces that can be reached.
    n_field_steps = math.floor(n_steps / 131)
    steps_from_centre = n_steps % len(grid.grid[0])
    # Positions: Key is the direction you come from.
    big_grid = Grid(np.tile(grid.grid, (3,3)))
    _, _, occ = get_occupancy(big_grid, add_positions(farmer_pos, (131, 131)), n_steps = steps_from_centre+len(grid.grid[0]))
    detiled = detile(occ.grid)
    things = {
        "NW": detiled[0],
        "N": detiled[1],
        "NE": detiled[2],
        "W": detiled[3],
        "C": detiled[4],
        "E": detiled[5],
        "SW": detiled[6],
        "S": detiled[7],
        "SE": detiled[8]
    }
    for k in things.keys():
        things[k] = count_occ(things[k])
    
    things["N"] = swap(things["N"])
    things["E"] = swap(things["E"])
    things["S"] = swap(things["S"])
    things["W"] = swap(things["W"])

    ans = 0
    ans += things["N"][0]
    ans += things["E"][0]
    ans += things["S"][0]
    ans += things["W"][0]
    ans += things["NE"][1] * (n_field_steps + 1)
    ans += things["NW"][1] * (n_field_steps + 1)
    ans += things["SE"][1] * (n_field_steps + 1)
    ans += things["SW"][1] * (n_field_steps + 1)

    # C (odd)
    # even/odd are in terms of steps from the origin
    state = 1
    central = things["C"]
    ans += central[state]
    for i in range(1,n_field_steps+1):
        state = (state + 1) % 2
        ans += central[state]*(i*4)
    return ans
                


def main(input_file):
    lines = input_file.split("\n")[:-1]
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.find("S")
            farmer_pos = (x,y)
            break
    grid = Grid(np.array([[1 if char == "#" else 0 for char in list(line)] for line in lines]))
    
    pt1_ans = solve_pt1(grid, farmer_pos, 64)
    pt2_ans = solve_pt2(grid, farmer_pos)
    return (pt1_ans, pt2_ans)