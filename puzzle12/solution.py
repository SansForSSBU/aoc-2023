
lines = []
with open("puzzle12/input.txt") as input:
    lines = input.read().split("\n")

lines = [line.split(" ") for line in lines]
conditions = [line[0] for line in lines]
criterias = [[int(x) for x in line[1].split(",")] for line in lines]
lines = list(zip(conditions, criterias))

def is_valid_configuration(line):
    criteria = line[1].copy()
    length = 0
    for char in line[0]:
        if char == "?":
            return True
        if char == "#":
            length += 1
        elif length > 0:
            if len(criteria) == 0 or criteria[0] != length:
                return False
            del criteria[0]
            length = 0
    return ((len(criteria) == 0 and length == 0) or (len(criteria) == 1 and criteria[0] == length))

def find_all_configurations(line):
    condition_report = line[0]
    if not is_valid_configuration(line):
        return []
    if condition_report.count("?") == 0:
        return [condition_report]
    possible_configurations = []
    possible_configurations = possible_configurations + find_all_configurations((condition_report.replace("?", "#", 1), line[1]))
    possible_configurations = possible_configurations + find_all_configurations((condition_report.replace("?", ".", 1), line[1]))
    return possible_configurations

def base_method(line):
    configs = find_all_configurations(line)
    valid_configs = [config for config in configs if is_valid_configuration([config, line[1]])]
    return len(valid_configs)

def solve_pt1():
    answer = 0
    for line in lines:
        answer += base_method(line)
    return answer

def unfold(reports):
    for n, report in enumerate(reports):
        new_report = ("?".join([report[0]]*5), report[1]*5)
        reports[n] = new_report
    return reports

def solve_pt2():
    return 0

print("Part 1:", solve_pt1())
lines = unfold(lines)
print("Part 2:", solve_pt2())


"""
I thought of a better solution, but I don't have the heart to get rid of this beautiful mess </3

def get_permutations(unk_block):
    if unk_block.count("?") == 0:
        return [unk_block]
    perms = []
    perms = perms + get_permutations(unk_block.replace("?", "#", 1))
    perms = perms + get_permutations(unk_block.replace("?", ".", 1))
    return perms

def get_met_criteria(block):
    criteria = []
    length = 0
    for char in block:
        if char == "#":
            length += 1
        elif length > 0:
            criteria.append(length)
            length = 0
    if length > 0:
        criteria.append(length)
    criteria = tuple(criteria)
    return criteria


pre_calced = {}

def get_meetable_criteria(unk_block):
    if pre_calced.get(unk_block, None):
        return pre_calced.get(unk_block)
    perms = get_permutations(unk_block)
    met_criteria = set([get_met_criteria(perm) for perm in perms])
    pre_calced[unk_block] = met_criteria
    return met_criteria

def split_criteria(criteria, meetable_criteria):
    possible_splits = []
    for crit in meetable_criteria:
        for window_start in range(len(criteria)+1):
            if window_start + len(crit) - 1 < len(criteria):
                x = criteria[window_start:window_start+len(crit)]
                if tuple(x) == crit:
                    possible_splits.append([criteria[:window_start], criteria[window_start+len(crit):]])

    return possible_splits

def lazy_check(problem):
    if problem[0].count("?") + problem[0].count("#") < sum(problem[1]):
        return False # Not enough possible ?'s to meet problem
    if problem[0].count("#") > sum(problem[1]):
        return False # Too many #'s for it to be possible
    return True

def create_subproblems(line):
    report = line[0]
    if report.count("?") == 0:
        return False
    end = 0
    all_subproblems = []
    while end < len(report):
        next_unknown = report.find("?", end)
        if next_unknown == -1:
            break
        end = report.find(".", next_unknown)
        if (end == -1):
            end = len(report)
        start = report.rfind(".", 0, end)+1
        unk_block = report[start:end]
        problem1_report = report[:start]
        problem2_report = report[end+1:]
        meetable_criteria = get_meetable_criteria(unk_block)
        split_criterias = split_criteria(line[1], meetable_criteria)

        subproblems = [[[problem1_report, c[0]], [problem2_report, c[1]]] for c in split_criterias]
        #subproblems = [subproblem for subproblem in subproblems if subproblem_pair_maybe_possible(subproblem)] # Subproblem doesn't even sound like a word anymore. It probably isn't.
        all_subproblems = all_subproblems + subproblems
    all_subproblems = [s for s in all_subproblems if lazy_check(s[0]) and lazy_check(s[1])]
    return all_subproblems


def magic(line):
    subproblems = create_subproblems(line)
    if subproblems == False:
        solutions = base_method(line)
        return solutions
    if len(subproblems) == 0:
        return 0
    solutions = 0
    for s in subproblems:
        solutions += magic(s[0]) * magic(s[1])
    return solutions

"""