import numpy as np
def get_adjacents(pos):
    (x, y) = pos
    adds = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for add in adds:
        yield (x + add[0], y + add[1])

def get_coords(grid, pos):
    (x, y) = pos
    if x > len(grid[0]) or x < 0:
        return -1
    if y > len(grid) or y < 0:
        return -1
    return grid[y][x]

def solve_pt1(grid, farmer_pos):
    positions = [farmer_pos]
    for i in range(64):
        next_positions = set([])
        for position in positions:
            next_positions.update(get_adjacents(position))
        positions = [pos for pos in list(next_positions) if get_coords(grid, pos) == 0]  
        print(i, len(positions))
    return len(positions)

def main(input_file):
    lines = input_file.split("\n")[:-1]
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.find("S")
            farmer_pos = (x,y)
            break
    grid = np.array([[1 if char == "#" else 0 for char in list(line)] for line in lines])
    
    pt1_ans = solve_pt1(grid, farmer_pos)
    return (pt1_ans, 0)