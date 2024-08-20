import string
lines = []

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


with open("puzzle3/input.txt") as input:
    lines = input.read().split("\n")

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

print(pt1_ans)