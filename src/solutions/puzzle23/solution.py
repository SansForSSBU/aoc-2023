import numpy as np
from copy import deepcopy
import os
import networkx as nx

def add_tuples(t1, t2):
    return tuple([int(x) for x in np.add(t1, t2)])

def get_adjacents(pos):
    moves = {
        "S": (0, 1), 
        "E": (1, 0), 
        "N": (0, -1), 
        "W":(-1, 0)
    }
    return {k: add_tuples(m, pos) for k, m in moves.items()}

class Maze():
    def __init__(self, char_arr, start_pos, curr_pos, end_pos):
        self.grid = np.char.array(char_arr)
        self.start_pos = start_pos
        self.curr_pos = curr_pos
        self.end_pos = end_pos
        self.steps = 0
    
    def set_pos(self, pos, char):
        (x,y) = pos
        self.grid[y,x] = char

    def get_char(self, pos):
        (x,y) = pos
        return self.grid[y,x]

    def is_in_grid(self, pos):
        return pos[0] in range(0, len(self.grid[0])) and pos[1] in range(0, len(self.grid))

    def get_moves(self, part2 = False):
        nexts = get_adjacents(self.curr_pos)
        valid_moves = []
        for dir, next in nexts.items():
            if not self.is_in_grid(next):
                continue
            if self.get_char(next) == "#":
                continue
            if not part2:
                if self.get_char(next) == "^" and dir == "S":
                    continue
                if self.get_char(next) == ">" and dir == "W":
                    continue
                if self.get_char(next) == "v" and dir == "N":
                    continue
                if self.get_char(next) == "<" and dir == "E":
                    continue
            valid_moves.append(next)
        return valid_moves
    
    def do_move(self, next_pos):
        self.set_pos(self.curr_pos, "#")
        self.curr_pos = next_pos
        self.steps += 1

    def at_end(self):
        return self.curr_pos == self.end_pos
    
    def is_junction(self, pos):
        if self.get_char(pos) != ".":
            return False
        adjacents = [adj for k, adj in get_adjacents(pos).items() if self.is_in_grid(adj) and self.get_char(adj) != "#"]
        return len(adjacents) > 2
    
    def get_junctions(self):
        junctions = []
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                pos = (x,y)
                if self.is_junction(pos):
                    junctions.append(pos)
        return junctions
    
    def to_graph(self, pt2=False):
        junctions = self.get_junctions()
        junctions = {f"j{k}":v for k,v in enumerate(junctions)}
        junctions["S"] = self.start_pos
        junctions["E"] = self.end_pos
        reverse_junctions_dict = {v:k for k,v in junctions.items()}
        G = nx.DiGraph()
        for k,v in junctions.items():
            maze_copy = deepcopy(self)
            maze_copy.curr_pos = v
            moves = maze_copy.get_moves(part2=pt2)
            for move in moves:
                m = deepcopy(maze_copy)
                m.do_move(move)
                while True:
                    if m.curr_pos in junctions.values():
                        j = reverse_junctions_dict[m.curr_pos]
                        G.add_edge(k, j, weight=m.steps)
                        break
                    nexts = m.get_moves(part2=pt2)
                    if len(nexts) > 1:
                        raise Exception()
                    if len(nexts) == 0:
                        break
                    m.do_move(nexts[0])

        return G

def solve_pt1(G):
    paths = nx.all_simple_paths(G, source='S', target='E')
    max_len = 0
    for path in paths:
        max_len = max(max_len, nx.path_weight(G, path, weight='weight'))
    return max_len

def main(input_file):
    l = [list(line) for line in input_file.split("\n") if len(line) > 0]
    start_pos = (l[0].index("."), 0)
    end_pos = (l[-1].index("."), len(l)-1)
    maze = Maze(l, start_pos, start_pos, end_pos)

    G = maze.to_graph()
    pt1_ans = solve_pt1(G)

    G = maze.to_graph(pt2=True)
    pt2_ans = solve_pt1(G)
    return (pt1_ans, pt2_ans)