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
    # 637538093080475 wrong
    # 637538116142463 wrong
    # 637538093080263 wrong
    # 637538116142675 wrong
    # 637537318244157 wrong
    # 637537318247987 wrong
    # First, just think about the spaces that can be reached.
    
    n_field_steps = n_steps // 131
    n_field_steps_odd_or_even = n_field_steps % 2
    steps_odd_or_even = n_steps % 2
    full_steps_from_centre = n_steps % 131
    # Positions: Key is the direction you come from.
    _, _, mid = get_occupancy(grid, farmer_pos, n_steps = min(n_steps, 300))
    big_grid = Grid(np.tile(grid.grid, (5,5)))
    _, _, occ = get_occupancy(big_grid, add_positions(farmer_pos, (262, 262)), n_steps = (n_steps % 131) + 131)
    detiled = detile(occ.grid, n=5)
    things = {
        "NW": detiled[6],
        "N": detiled[2],
        "NE": detiled[8],
        "W": detiled[10],
        "C": mid.grid,
        "E": detiled[14],
        "SW": detiled[16],
        "S": detiled[22],
        "SE": detiled[18]
    }
    for k in things.keys():
        things[k] = count_occ(things[k])
    
    flood = things["C"]

    ans = 0
    ans += flood[steps_odd_or_even%2]
    # Because steps is odd, but fields crossed is even and this is n+1 these should be the even cases
    edges_even_or_odd = (n_steps + n_field_steps + 1) % 2
    ans += things["N"][edges_even_or_odd]
    ans += things["E"][edges_even_or_odd]
    ans += things["S"][edges_even_or_odd]
    ans += things["W"][edges_even_or_odd]
    ans += things["NE"][edges_even_or_odd] * (n_field_steps)
    ans += things["NW"][edges_even_or_odd] * (n_field_steps)
    ans += things["SE"][edges_even_or_odd] * (n_field_steps)
    ans += things["SW"][edges_even_or_odd] * (n_field_steps)

    # C (odd)
    # even/odd are in terms of steps from the origin
    state = steps_odd_or_even
    for i in range(1,n_field_steps+1):
        state = (state + 1) % 2
        ans += flood[state]*(i*4)
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
    verification_grid = Grid(np.tile(grid.grid, (3,3)))
    n = 130
    a = solve_pt1(verification_grid, add_positions(farmer_pos, (131,131)), n)
    b = solve_pt2(grid, farmer_pos, n)
    print(a,b)
    pt2_ans = solve_pt2(grid, farmer_pos)
    return (pt1_ans, pt2_ans)