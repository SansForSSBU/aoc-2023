
with open("puzzle9/input.txt") as input:
    lines = input.read().split("\n")

lines = [[int(val) for val in line.split(" ")] for line in lines]

def get_differences(line):
    val_ptr = 0
    next_line = []
    while val_ptr < len(line)-1:
        next_line.append(line[val_ptr + 1] - line[val_ptr])
        val_ptr += 1
    return next_line

def get_all_differences(line):
    my_lines = [line]
    while True:
        my_lines.append(get_differences(my_lines[-1]))
        if len(my_lines[-1]) == my_lines[-1].count(0):
            break
    return my_lines

def extrapolate(line_diffs):
    prev_val = 0
    line_diffs.reverse()
    for line in line_diffs:
        next_val = line[-1]+prev_val
        line.append(next_val)
        prev_val = next_val
    line_diffs.reverse()
    return line_diffs[0][-1]

def solve_pt1():
    result = 0
    for line in lines:
        line_diffs = get_all_differences(line)
        last_num = line[-1]
        diff_len = len(line_diffs)
        extrapolation = extrapolate(line_diffs)
        result += extrapolation
    return result

def solve_pt2():
    global lines
    lines = [list(reversed(line)) for line in lines]
    return solve_pt1()

print(solve_pt1())
print(solve_pt2())