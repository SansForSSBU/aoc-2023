
lines = []
with open("puzzle13/input.txt") as input:
    lines = input.read().split("\n")

images = []
next_image = []
for line in lines:
    if line == "":
        images.append(next_image)
        next_image = []
    else:
        next_image.append(line)
images.append(next_image)

def get_column(map, x):
    column = "".join([line[x] for line in map])
    return column

def get_row(map, y):
    return map[y]

b32_repr = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F",
    16: "G",
    17: "H",
    18: "I",
    19: "J",
    20: "K",
    21: "L",
    22: "M",
    23: "N",
    24: "O",
    25: "P",
    26: "Q",
    27: "R",
    28: "S",
    29: "T",
    30: "U",
    31: "V"
}

def print_image(image, x_reflects, y_reflects):
    nums = "".join([b32_repr.get(n, "!") for n, x in enumerate(image[0])])
    print(nums)
    l2 = [" "]*len(image[0])
    for pair in x_reflects:
        l2[pair[0]] = ">"
        l2[pair[1]] = "<"
    l3 = "".join(l2)
    print(l3)
    for n, line in enumerate(image):
        arrow = " "
        if n in [y[0] for y in y_reflects]:
            arrow = "v"
        if n in [y[1] for y in y_reflects]:
            arrow = "^"
        print(line, arrow, b32_repr.get(n, "!"))
    

def find_reflection_lines(image):
    x_reflects = []
    y_reflects = []
    for x in range(0, len(image[0])-1):
        x1 = x
        x2 = x + 1
        while True:
            if get_column(image, x1) == get_column(image, x2):
                x1 -= 1
                x2 += 1
                if x2 >= len(image[0]) or x1 < 0:
                    x_reflects.append((x, x+1))
                    break
            else:
                break

    for y in range(0, len(image)-1):
        y1 = y
        y2 = y + 1
        while True:
            if get_row(image, y1) == get_row(image, y2):
                y1 -= 1
                y2 += 1
                if y2 >= len(image) or y1 < 0:
                    y_reflects.append((y, y+1))
                    break
            else:
                break
    return x_reflects, y_reflects

def summarise_notes(x_reflects, y_reflects):
    x_summary = sum([l[1] for l in x_reflects])
    y_summary = sum([l[1] for l in y_reflects])
    return (100*y_summary)+x_summary

def solve_pt1():
    result = 0
    for image in images:
        mirrors = find_reflection_lines(image)
        x_reflects = mirrors[0]
        y_reflects = mirrors[1]
        summary = summarise_notes(mirrors[0], mirrors[1])
        #print(" ")
        #print_image(image, x_reflects, y_reflects)
        #print("Answer: ", summarise_notes(x_reflects, y_reflects))
        result += summary
    return result

def solve_pt2():
    return 0

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())