import math
from sympy import symbols, linsolve, EmptySet
from copy import deepcopy


t = symbols('t', real=True)

class Particle():
    def set_self_pos(self, time_symbol):
        self.x = time_symbol*self.v[0] + self.p[0]
        self.y = time_symbol*self.v[1] + self.p[1]
        self.z = time_symbol*self.v[2] + self.p[2]

    def __init__(self, input_line):        
        pos, vel = input_line.split("@")
        self.p = [int(x) for x in pos.split(",")]
        self.v = [int(x) for x in vel.split(",")]
        self.set_self_pos(t)

def is_in_test_area(pos):
    if pos[0] >= 200000000000000 and pos[0] <= 400000000000000:
        if pos[1] >= 200000000000000 and pos[1] <= 400000000000000:
            return True
    return False

def main(input_file):
    pt1_ans = 0
    particles = [Particle(x) for x in input_file.split("\n") if len(x) != 0]
    for idx, p1 in enumerate(particles):
        for p2 in particles[idx+1:]:
            t1 = symbols('t1', real=True)
            t2 = symbols('t2', real=True)
            a = deepcopy(p1)
            b = deepcopy(p2)
            a.set_self_pos(t1)
            b.set_self_pos(t2)
            solved = list(linsolve([a.x - b.x, a.y - b.y], (t1, t2)))
            if len(solved) > 1:
                raise Exception
            if len(solved) == 0:
                continue
            if is_in_test_area(solved[0]):
                pt1_ans += 1
            pass
    
    return (pt1_ans, 0)