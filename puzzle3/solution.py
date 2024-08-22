import string
lines = []
with open("puzzle3/input.txt") as input:
    lines = input.read().split("\n")

def get_adjacent_digit_coords(coord):
    coords = []
    for y in range(coord[1]-1, coord[1]+2):
        if y >= len(lines) or y < 0:
            continue

        line = lines[y]
        for x in range(coord[0]-1, coord[0]+2):
            if x >= len(line) or x < 0:
                continue
            if line[x].isnumeric():
                coords.append((x, y))
    return coords

def get_symbol_coords():
    coords = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (char != '.' and char in string.punctuation):
                coords.append((x, y))
    return coords

def get_gear_coords():
    coords = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (char == '*'):
                coords.append((x, y))
    return coords

def filter_digits(digits):
    min_x = min([digit[0] for digit in digits])
    for x in range(min_x, min_x + 3):
        digits_to_remove = []
        for digit in digits:
            if digit[0] != x:
                continue
            if (digit[0] + 1, digit[1]) in digits:
                digits_to_remove.append(digit)
        for digit in digits_to_remove:
            digits.remove(digit)
    return digits

def read_digit(coord):
    line = lines[coord[1]]
    while True:#Seek start
        if coord[0] == 0:
            break
        if not line[coord[0]-1].isnumeric():
            break
        coord = (coord[0]-1, coord[1])
    digit = line[coord[0]]
    while True:#Seek end
        if coord[0]+1 >= len(line):
            break
        if not line[coord[0]+1].isnumeric():
            break
        coord = (coord[0]+1, coord[1])
        digit += line[coord[0]]
    return int(digit)

def calc_gear(gear_coords):
    digits = get_adjacent_digit_coords(gear_coords)
    digits = filter_digits(digits)
    if len(digits) != 2:
        return 0
    return read_digit(digits[0])*read_digit(digits[1])
    
def solve_pt1():
    symbol_coords = get_symbol_coords()
    digits_next_to_symbols = []
    for coord in symbol_coords:
        digits_next_to_symbols += get_adjacent_digit_coords(coord)
    pt1_ans = 0
    for y, line in enumerate(lines):
        num_str = "0"
        next_to_symbol = False
        for x, char in enumerate(line):
            if char.isnumeric():
                num_str = num_str + char
                if (x, y) in digits_next_to_symbols:
                    next_to_symbol = True
            else:#Reached end of a number, or we're at the start of a line
                #print(num_str)
                if (next_to_symbol):
                    pt1_ans += int(num_str)
                num_str = "0"
                next_to_symbol = False

        if (next_to_symbol):
            pt1_ans += int(num_str)
        num_str = "0"
        next_to_symbol = False
    return pt1_ans

def solve_pt2():
    pt2_ans = 0
    gear_coords = get_gear_coords()
    for gear_coord in gear_coords:
        pt2_ans += calc_gear(gear_coord)
    return pt2_ans

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())