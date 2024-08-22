
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
        if char == "#":
            length += 1
        elif length > 0:
            if len(criteria) == 0 or criteria[0] != length:
                return False
            del criteria[0]
            length = 0
    return ((len(criteria) == 0 and length == 0) or (len(criteria) == 1 and criteria[0] == length))

def find_all_configurations(condition_report):
    if condition_report.count("?") == 0:
        return [condition_report]
    possible_configurations = []
    possible_configurations = possible_configurations + find_all_configurations(condition_report.replace("?", "#", 1))
    possible_configurations = possible_configurations + find_all_configurations(condition_report.replace("?", ".", 1))
    return possible_configurations

def solve_pt1():
    answer = 0
    for line in lines:
        configs = find_all_configurations(line[0])
        valid_configs = [config for config in configs if is_valid_configuration([config, line[1]])]
        answer += len(valid_configs)
    return answer

def unfold(reports):
    for n, report in enumerate(reports):
        new_report = ("?".join([report[0]]*5), report[1]*5)
        reports[n] = new_report
    return reports

print("Part 1:", solve_pt1())
print(lines[0])
lines = unfold(lines)
print(lines[0])
print("Part 2:", solve_pt1())