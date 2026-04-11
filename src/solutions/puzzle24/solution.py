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
            #intersect_b = (p2.x.subs(t, t2_val), p2.y.subs(t, t2_val))
            if is_in_test_area(intersect_a):
                pt1_ans += 1
            pass
    return pt1_ans

def example_problem():
    t1, t2, t3, t4, t5 = symbols("t1 t2 t3 t4 t5", real=True)
    lines = [
        "19, 13, 30 @ -2, 1, -2",
        "18, 19, 22 @ -1, -1, -2",
        "20, 25, 34 @ -2, -2, -4",
        "12, 31, 28 @ -1, -2, -1",
        "20, 19, 15 @ 1, -5, -3"
    ]
    sym = [t1, t2, t3, t4, t5]
    particles = [Particle(p) for p in lines]
    for idx, particle in enumerate(particles):
        pass
        time_sym = sym[idx]
        particle.set_self_pos(time_sym)

    pass

def full_problem(particles):
    t_values = np.array([part.v[0] for part in particles])
    p_values = np.array([part.p[0] for part in particles])
    
    m, c = np.polyfit(t_values, p_values, 1)
    pass

def main(input_file):
    particles = [Particle(x) for x in input_file.split("\n") if len(x) != 0]
    for idx, particle in enumerate(particles):
        pass
        time_sym = symbols(f"t{idx+1}", real=True)
        particle.set_self_pos(time_sym)
    pt1_ans = 0#solve_pt1(particles)
    particles = [v for k,v in enumerate(particles)]
    x_pairs = [(p.v[0], p.p[0]) for p in particles]
    vels = [p[0] for p in x_pairs]
    unique_vels = list(set(vels))
    three_vels = [v for v in unique_vels if vels.count(v) == 3]
    t1, t2, t3, c, m = symbols("t1 t2 t3 c m", real=True)
    my_eqs = []
    for three in three_vels:
        positions = sorted([pair[1] for pair in x_pairs if pair[0] == three])
        eq_1 = (m-three)*t1 + c - positions[0]
        eq_2 = (m-three)*t2 + c - positions[1]
        eq_3 = (m-three)*t3 + c - positions[2]
        eq_1 = eq_1.subs(t1, 0)
        eq_2 = eq_2.subs(t2, 1)
        solutions = solve([eq_1, eq_2, eq_3], (t3, c, m))
        if len(solutions) != 1:
            raise Exception()
        _, val_c, val_m = solutions[0]
        my_eqs.append(val_m)
        print(solutions)
        pass
    pass
    
    
    return (pt1_ans, 0)