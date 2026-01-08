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
    
    def get_adjacents(self, pos):
        (x, y) = pos
        adds = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for add in adds:
            yield (x + add[0], y + add[1])

    def is_rock(self, pos):
        return self.get_coords(pos) == 1

def add_positions(a,b):
    return (a[0]+b[0], a[1]+b[1])

def solve_pt1(grid, farmer_pos):
    positions = [farmer_pos]
    for i in range(64):
        next_positions = set([])
        for position in positions:
            next_positions.update(grid.get_adjacents(position))
        positions = next_positions
        positions = list(filter(grid.is_in_grid, positions))
        positions = list(filter(lambda x: not grid.is_rock(x), positions))
    return len(list(positions))

def solve_pt2(grid, farmer_pos):
    positions = {
        farmer_pos: set([(0, 0)])
    }
    steps = 26501365
    for i in range(steps):
        next_positions = {}
        for pos,PUs in positions.items():
            adjacents = grid.get_adjacents(pos)
            for adj in adjacents:
                pu_offset = grid.get_pu_offset(adj)
                contributions = [add_positions(pu, pu_offset) for pu in PUs]
                existing = next_positions.get(adj, None)
                if existing == None:
                    existing = set([])
                existing.update(contributions)
                next_positions[adj] = existing
                pass
        positions = next_positions
        if i % 1000 == 0:
            print(i)
    return sum(sum(len(v)) for v in positions.values())
                


def main(input_file):
    lines = input_file.split("\n")[:-1]
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.find("S")
            farmer_pos = (x,y)
            break
    grid = Grid(np.array([[1 if char == "#" else 0 for char in list(line)] for line in lines]))
    
    pt1_ans = solve_pt1(grid, farmer_pos)
    pt2_ans = 0#solve_pt2(grid, farmer_pos)
    return (pt1_ans, pt2_ans)