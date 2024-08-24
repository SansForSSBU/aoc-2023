from enum import Enum
import operator
import copy

lines = []
with open("puzzle17/input.txt") as input:
    lines = input.read().split("\n")
lines = [[int(x) for x in list(line)] for line in lines]



class D(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3



def go_direction(pos, direction):
    if direction == D.NORTH:
        return (pos[0], pos[1] - 1)
    elif direction == D.EAST:
        return (pos[0] + 1, pos[1])
    elif direction == D.SOUTH:
        return (pos[0], pos[1] + 1)
    elif direction == D.WEST:
        return (pos[0] - 1, pos[1])

def get_tile(grid, coords):
    if coords[0] < 0 or coords[0] >= len(grid[0]) or coords[1] < 0 or coords[1] >= len(grid[1]):
        return None
    return grid[coords[1]][coords[0]]

LR_turns = {
    D.NORTH: (D.EAST, D.WEST),
    D.EAST: (D.NORTH, D.SOUTH),
    D.SOUTH: (D.WEST, D.EAST),
    D.WEST: (D.SOUTH, D.NORTH)
}

class State:
    def __init__(self, coords, direction, tiles_left, cost):
        self.coords = coords
        self.dir = direction
        self.tiles_left = tiles_left
        self.cost = cost
    
    # Two states with different costs will be considered equal.
    def __eq__(self, other):
        return self.coords == other.coords and self.dir == other.dir and self.tiles_left == other.tiles_left

    def move_1_tile(self):
        self.coords = go_direction(self.coords, self.dir)
        self.tiles_left -= 1

    def get_next_states(self, map):
        next_states = []
        if self.tiles_left > 0:
            state = copy.deepcopy(self)
            state.move_1_tile()
            next_states.append(state)
        if max_path_length - self.tiles_left >= min_path_length:
            for direction in LR_turns[self.dir]:
                state = copy.deepcopy(self)
                state.tiles_left = max_path_length
                state.dir = direction
                state.move_1_tile()
                next_states.append(state)
        next_states = [state for state in next_states if get_tile(map, state.coords) is not None]
        for state in next_states:
            state.cost += get_tile(map, state.coords)
        return next_states
        
        
        

checked_states = {}
def add_to_checked_states(state):
    checked_states[state.coords] = checked_states.get(state.coords, []) + [state]
def state_has_been_checked(state):
    return state in checked_states.get(state.coords, [])

def solve_pt1():
    states_checked = 0
    states = [State((0, 0), d, max_path_length, 0) for d in [D.EAST, D.SOUTH]]
    while len(states) > 0:
        states.sort(key=lambda x: x.cost)
        state = states[0]
        del states[0]
        add_to_checked_states(state)
        if states_checked % 1000 == 0:
            print(states_checked)
        states_checked += 1
        next_states = state.get_next_states(lines)
        for state in next_states:
            if state_has_been_checked(state):
                continue
            duplicate = next((x for x in states if x == state), None)
            if duplicate is None:
                states.append(state)
            else:
                duplicate.cost = min(state.cost, duplicate.cost)
            
    end_cost = min([state.cost for state in checked_states[(140,140)] if (max_path_length-state.tiles_left >= min_path_length)])
    return end_cost

pt1 = True
pt2 = False
if pt1:
    min_path_length = 1
    max_path_length = 3
    print("Part 1:", solve_pt1())
if pt2:
    min_path_length = 4
    max_path_length = 10
    print("Part 2:", solve_pt1())