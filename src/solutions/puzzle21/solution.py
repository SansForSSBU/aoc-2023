import numpy as np

class Grid():
    def __init__(self, grid):
        self.grid = grid

    def is_in_grid(self, pos):
        (x, y) = pos
        if x > len(self.grid[0]) or x < 0:
            return False
        if y > len(self.grid) or y < 0:
            return False
        return True

    def get_coords(self, pos):
        (x, y) = pos
        if not self.is_in_grid(pos):
            return -1
        return self.grid[y][x]
    
    def get_adjacents(self, pos):
        (x, y) = pos
        adds = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for add in adds:
            yield (x + add[0], y + add[1])



def solve_pt1(grid, farmer_pos):
    positions = [farmer_pos]
    for i in range(64):
        next_positions = set([])
        for position in positions:
            next_positions.update(grid.get_adjacents(position))
        positions = [pos for pos in list(next_positions) if grid.get_coords(pos) == 0]  
    return len(positions)

def solve_pt2(grid, farmer_pos):
    positions = {farmer_pos: [(0, 0)]}
    steps = 26501365


def main(input_file):
    lines = input_file.split("\n")[:-1]
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.find("S")
            farmer_pos = (x,y)
            break
    grid = Grid(np.array([[1 if char == "#" else 0 for char in list(line)] for line in lines]))
    
    pt1_ans = solve_pt1(grid, farmer_pos)
    return (pt1_ans, 0)