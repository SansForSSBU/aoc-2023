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
    
    def convert_to_grid_detection_pos(self, pos):
        (x, y) = pos
        x = x % len(self.grid[0])
        y = y % len(self.grid)
        return (x,y)

    def get_coords(self, pos):
        (x, y) = pos
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
            if not self.is_rock(extra_pos):
                yield extra_pos

    def is_rock(self, pos):
        grid_detection_pos = self.convert_to_grid_detection_pos(pos)
        return self.get_coords(grid_detection_pos) == 1

def add_positions(a,b):
    return (a[0]+b[0], a[1]+b[1])

def get_supergrid_pos(pos):
    return (pos[0] // 131, pos[1] // 131)

def solve_pt1(grid, farmer_pos, num_steps):
    reached = np.zeros(grid.grid.shape)
    reached[farmer_pos[1], farmer_pos[0]] = 1
    positions = [farmer_pos]
    steps_to = {farmer_pos: 0}
    for step in range(1, num_steps+1):
        next_positions = []
        for position in positions:
            for next in grid.get_adjacents(position):
                if reached[next[1], next[0]] == 1:
                    continue
                reached[next[1], next[0]] = 1
                steps_to[next] = min(step, steps_to.get(next, math.inf))
                next_positions.append(next)
        positions = next_positions
    return len([k for k,v in steps_to.items() if v % 2 == num_steps % 2])

def solve_pt2(grid, farmer_pos, num_steps):
    reached = np.zeros([grid.grid.shape[0]*(1+(num_steps%131)), grid.grid.shape[1]*(1+(num_steps%131))])
    reached[farmer_pos[1], farmer_pos[0]] = 1
    positions = [farmer_pos]
    steps_to = {farmer_pos: 0}
    for step in range(1, num_steps+1):
        next_positions = []
        for position in positions:
            for next in grid.get_adjacents(position):
                if reached[next[1], next[0]] == 1:
                    continue
                reached[next[1], next[0]] = 1
                steps_to[next] = min(step, steps_to.get(next, math.inf))
                next_positions.append(next)
        positions = next_positions
    num_subgrids = {}
    for k,v in steps_to.items():
        if v % 2 != num_steps % 2:
            continue
        snapped = grid.convert_to_grid_detection_pos(k)
        num_subgrids[snapped] = num_subgrids.get(snapped, 0) + 1
    return num_subgrids, len([k for k,v in steps_to.items() if v % 2 == num_steps % 2])

def main(input_file):
    lines = input_file.split("\n")[:-1]
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.find("S")
            farmer_pos = (x,y)
            break
    grid = Grid(np.array([[1 if char == "#" else 0 for char in list(line)] for line in lines]))
    
    pt1_ans = solve_pt1(grid, farmer_pos, 64)
    steps = 65+131
    pt2_key, a = solve_pt2(grid, add_positions(farmer_pos, (131*((steps // 131)+1), 131*((steps // 131)+1))), steps)
    pt2_ans = 0
    n = 26501365 // 131
    #n = 1
    conv = {
        1: n*n,
        2: (n*n) + n,
        4: (n+1)*(n+1)
    }
    for v in pt2_key.values():
        pt2_ans += conv[v]
    return (pt1_ans, pt2_ans)