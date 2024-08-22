
lines = []
with open("puzzle6/input.txt") as input:
    lines = input.read().split("\n")

time = [int(x) for x in [x for x in lines[0].split(" ") if len(x) > 0][1:]]
distance = [int(x) for x in [x for x in lines[1].split(" ") if len(x) > 0][1:]]
records = list(zip(time, distance))

from math import sqrt, ceil
def calculate_distance(time, hold):
    return (time-hold)*hold

def button_holds(record):
    ways = 0
    time = record[0]
    distance = record[1]
    for t in range(time):
        if calculate_distance(time, t+1) >= distance:
            ways += 1
    return ways

def solve_pt1():
    ans = 1
    for record in records:
        ans = ans * button_holds(record)
    return ans

def solve_pt2():
    full_time = ""
    for i in time:
        full_time = full_time + str(i)
    full_time = int(full_time)
    full_distance = ""
    for i in distance:
        full_distance = full_distance + str(i)
    full_distance = int(full_distance)
    return button_holds([full_time, full_distance])

print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())