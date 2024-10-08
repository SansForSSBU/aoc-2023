import math

translation = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}
def interpret(num):
    if translation.get(num) != None:
        return translation.get(num)
    elif translation.get(num[::-1]) != None:
        return translation.get(num[::-1])
    return num

def find_first_number(line, nums):
    lowest_index = math.inf
    first_num = "0"
    for num in nums:
        idx = line.find(num)
        if (idx == -1):
            continue
        if idx <= lowest_index:
            first_num = interpret(num)
            lowest_index = idx
    return first_num

nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
reversed_nums = [num[::-1] for num in nums]

pt1_ans = 0
pt2_ans = 0

with open("puzzle1/input.txt") as f:
    lines=f.read().split("\n")
    for line in lines:

        first = find_first_number(line, nums[:9])
        last = find_first_number(line[::-1], reversed_nums[:9])
        num = int(first+last)
        pt1_ans += num

        first = find_first_number(line, nums)
        last = find_first_number(line[::-1], reversed_nums)
        num = int(first+last)
        pt2_ans += num

print("Part 1:", pt1_ans)
print("Part 2:", pt2_ans)