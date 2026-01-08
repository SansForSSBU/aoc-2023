from math import lcm
def main(input_file):
    lines = input_file.split("\n")[:-1]

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

    pt1_ans = solve_pt1()
    pt2_ans = solve_pt2()

    return (pt1_ans, pt2_ans)