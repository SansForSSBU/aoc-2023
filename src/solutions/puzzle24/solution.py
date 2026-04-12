import math
from sympy import symbols, linsolve, nonlinsolve, EmptySet, solve
from copy import deepcopy
import numpy as np


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

def solve_pt1(particles):
    pt1_ans = 0
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
            t1_val, t2_val = solved[0]
            if t1_val < 0 or t2_val < 0:
                continue
            intersect_a = (p1.x.subs(t, t1_val), p1.y.subs(t, t1_val))
            if is_in_test_area(intersect_a):
                pt1_ans += 1
            pass
    return pt1_ans

def main(input_file):
    particles = [Particle(x) for x in input_file.split("\n") if len(x) != 0]
    pt1_ans = solve_pt1(particles)
    particles = [Particle(x) for x in input_file.split("\n") if len(x) != 0]
    x_positions = [part.p[0] for part in particles]
    print([a for a in x_positions if x_positions.count(a) > 1])
    y_positions = [part.p[1] for part in particles]
    print([a for a in y_positions if y_positions.count(a) > 1])
    z_positions = [part.p[2] for part in particles]
    print([a for a in z_positions if z_positions.count(a) > 1])

    yc = 273305746686315
    ym = 15
    destroyer_y_eq = yc + ym*t
    t1 = solve([particles[0].y - destroyer_y_eq], t)[t]
    t2 = solve([particles[1].y - destroyer_y_eq], t)[t]
    m, c = symbols("m c", real=True)
    x_eqs = [
        particles[0].x.subs(t, t1) - (m*t1 + c),
        particles[1].x.subs(t, t2) - (m*t2 + c)
    ]
    res = solve(x_eqs, (m, c))
    xc = res[c]
    xm = res[m]
    m, c = symbols("m c", real=True)
    z_eqs = [
        particles[0].z.subs(t, t1) - (m*t1 + c),
        particles[1].z.subs(t, t2) - (m*t2 + c)
    ]
    res = solve(z_eqs, (m, c))
    zc = res[c]
    zm = res[m]
    pt2_ans = xc + yc + zc
    pt2_ans = int(pt2_ans)

    return (pt1_ans, pt2_ans)