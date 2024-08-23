import math

lines = []
with open("puzzle12/input.txt") as input:
    lines = input.read().split("\n")

lines = [line.split(" ") for line in lines]
conditions = [line[0] for line in lines]
criterias = [[int(x) for x in line[1].split(",")] for line in lines]
lines = list(zip(conditions, criterias))

def unfold(reports):
    for n, report in enumerate(reports):
        new_report = ("?".join([report[0]]*5), report[1]*5)
        reports[n] = new_report
    return reports

def latest_first_criteria_meet(line):
    earliest_space = line[0].find(".", line[0].find("#"))
    if earliest_space == -1:
        earliest_space = len(line[0])
    first_overflow = line[0].find("#"*(line[1][0]+1))
    if first_overflow == -1:
        first_overflow = math.inf
    others_impossible_at = len(line[0]) - (sum(line[1][1:]) + len(line[1][1:]))
    return min(earliest_space-1, first_overflow-2, others_impossible_at-1)

def can_meet_criteria_0_at(line, pos):
    l = line[0][:pos+1]
    if pos+1 < len(line[0]) and line[0][pos+1] == "#":
        return False
    first_hash = l.find("#")
    min_line_length = 0
    if first_hash != -1:
        min_line_length = pos - first_hash + 1
    max_line_length = 0
    for chr in reversed(l):
        if chr == ".":
            break
        max_line_length += 1
    required_length = line[1][0]
    ret = (min_line_length <= required_length and max_line_length >= required_length)
    return ret

def new_method(line):
    new_dict = {}
    old_dict = {0: 1}
    curr_positions = [0]
    conds = line[1].copy()
    while len(conds) > 0:
        new_dict = {}
        next_positions = set()
        for curr_pos in curr_positions:
            l = [line[0][curr_pos:], conds]
            this_next_positions = set()
            last = latest_first_criteria_meet(l)
            for i in range(last+1):
                if can_meet_criteria_0_at(l, i):
                    next_positions.add(i+2+curr_pos)
                    this_next_positions.add(i+2+curr_pos)
            for pos in this_next_positions:
                new_dict[pos] = new_dict.get(pos, 0) + old_dict[curr_pos]
        curr_positions = next_positions
        del conds[0]
        old_dict = new_dict
    result = 0
    for k in new_dict.keys():
        if line[0].find("#", k) == -1:
            result += new_dict[k]
    return result

def solve_pt1():
    ans = 0
    for line in lines:
        ans += new_method(line)
    return ans

print("Part 1:", solve_pt1())
lines = unfold(lines)
print("Part 2:", solve_pt1())