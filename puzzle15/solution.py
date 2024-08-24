
non_label_strings = ["=", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
lines = []
with open("puzzle15/input.txt") as input:
    lines = input.read().split(",")



def hash(string):
    hash = 0
    for char in string:
        hash += ord(char)
        hash = hash * 17
        hash = hash % 256
    return hash

def calculate_focal_power(box_no, box, focal):
    ans = 0
    for n, lens in enumerate(box):
        ans += (box_no+1)*(n+1)*focal[lens]
    return ans

def remove_strings(base_str, str_list):
    for string in str_list:
        base_str = base_str.replace(string, "")
    return base_str


def solve_pt1():
    return sum([hash(string) for string in lines])

def solve_pt2():
    focals = [{} for _ in range(256)]
    boxes = [[] for _ in range(256)]
    for operation in lines:
        label = remove_strings(operation, non_label_strings)
        box_no = hash(label)
        if operation.find("-") != -1:
            if label in boxes[box_no]: 
                boxes[box_no].remove(label)
        elif operation.find("=") != -1:
            focal = int(operation.split("=")[1])
            if not label in boxes[box_no]:
                boxes[box_no].append(label)
            focals[box_no][label] = focal
    ans = 0
    for box_no, box_info in enumerate(zip(boxes, focals)):
        box = box_info[0]
        focal = box_info[1]
        focal_power = calculate_focal_power(box_no, box, focal)
        ans += focal_power
    return ans

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())