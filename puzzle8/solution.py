from math import lcm

lines = []
with open("puzzle8/input.txt") as input:
    lines = input.read().split("\n")

sequence = lines[0]
sequence = sequence.replace("L", "0")
sequence = sequence.replace("R", "1")
mappings = lines[2:]
mappings = [x.replace("=", "") for x in mappings]
mappings = [x.replace("(", "") for x in mappings]
mappings = [x.replace(")", "") for x in mappings]
mappings = [x.replace(",", "") for x in mappings]
mappings = [x.split(" ") for x in mappings]
direction_dict = {}
for mapping in mappings:
    del mapping[1]
    direction_dict[mapping[0]] = (mapping[1], mapping[2])

def solve_pt1():
    location = "AAA"
    steps = 0
    while True:
        for letter in sequence:
            location = direction_dict[location][int(letter)]
            steps += 1
            if location == "ZZZ":
                return steps

def goto_next(location, sequence_ptr):
    return direction_dict[location][int(sequence[sequence_ptr])]

def next_seq_ptr(sequence_ptr):
    if sequence_ptr < len(sequence)-1:
        return sequence_ptr+1
    else:
        return 0

def find_cycle(location):
    last_done = {}
    visited_locations = []
    Z_locations = []
    steps = 0
    seq_ptr = 0
    while True:
        deets = (location, seq_ptr)
        # Check if we're at a Z
        if location[2] == "Z":
            Z_locations.append(steps)
        # Check if we've been in the same situation before
        if visited_locations.count(deets) > 0:
            cycle_offset = last_done[deets]
            cycle_len = steps - cycle_offset
            Z_offsets = [Z-cycle_offset for Z in Z_locations]
            return (Z_locations, cycle_len)#(Z_offsets, cycle_len)
        last_done[deets] = steps
        visited_locations.append(deets)
        # Advance one step
        steps += 1
        location = goto_next(location, seq_ptr)
        seq_ptr = next_seq_ptr(seq_ptr)

def solve_pt2():
    locations = [x for x in list(direction_dict.keys()) if x[2] == "A"]
    cycles = [find_cycle(location) for location in locations]
    cycles = [[cycle[0][0], cycle[1]] for cycle in cycles]
    return lcm(*[cycle[0] for cycle in cycles])

print(solve_pt1())
print(solve_pt2())


"""
Didn't have to do any of this, LOL. 
I was tearing my hair out trying to figure out how to find where any two arbitrary cycles join. I couldn't figure it out.
However, by a totally meaningless coincidence, 'Z' happens to be the same number of steps away from the start as itself in the cycle.
The puzzle setter probably did that to make the puzzle easier.
So we only need to find the combined cycle length, which is just the LCM of all cycle lengths.

def fast_join_cycles(cycle1, cycle2):
    return [find_common_point(cycle1, cycle2), lcm(cycle1[1], cycle2[1])]

def find_common_point(c1, c2):
    print(c1, c2)
    common_cycle_length = lcm(c1[1], c2[1])
    print((c1[0] + common_cycle_length) % c2[1])

def zero_offset(cycle):
    return [x-cycle[0] for x in cycle[1]]


def join_cycles(cycle1, cycle2):
    cycle1 = cycle1.copy()
    cycle2 = cycle2.copy()
    while cycle1[0] != cycle2[0]:
        if cycle1[0] < cycle2[0]:
            cycle1[0] += cycle1[1]
        else:
            cycle2[0] += cycle2[1]
    return [cycle1[0], lcm(cycle1[1], cycle2[1])]
"""