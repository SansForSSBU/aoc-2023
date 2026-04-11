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
    t, t1, t2, t3, t4, t5 = symbols("t t1 t2 t3 t4 t5", real=True)
    m, c = symbols("m c", real=True)
    p = m*t + c
    
    p1 = 19 - 2*t1
    p2 = 18 - t2
    p3 = 20 - 2*t3
    p4 = 12 - t4
    p5 = 20 + t5

    eqs = [
        p.subs(t, t1) - p1,
        p.subs(t, t2) - p2,
        p.subs(t, t3) - p3,
        p.subs(t, t4) - p4,
        p.subs(t, t5) - p5
    ]
    finds = (t1, t2, t3, t4, t5, c, m)
    times = solve(eqs, finds)
    
    diffs = [
        times[t1] - times[t3]
    ]
    pass

    eqs = [
        p.subs(t, t1) - p1,
        p.subs(t, t2) - p2,
        p.subs(t, t3) - p3,
        #t1 - t2 - 2, # Outside information
        #t1 - t3 - 1 # Outside information
    ]
    finds = (t1, t2, t3, c, m)
    solutions = solve(eqs, finds)
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
    example_problem()
    #eqs = [particle.x for particle in particles]
    pass
    full_problem(particles)
    destroyer_m = symbols("des_m", real=True)
    destroyer_c = symbols("des_c", real=True)
    destroyer_t = symbols("des_t", real=True)
    destroyer_eq = (destroyer_m * destroyer_t) + destroyer_c
    dest_eqs = []
    time_coefficients = []
    for first_eq in eqs[:5]:
        t = list(first_eq.free_symbols)[0]
        time_coefficients.append(t)
        dest_eq = destroyer_eq.subs(destroyer_t, t)
        pass
        dest_eqs.append(dest_eq - first_eq)
    pass
    
    
    return (pt1_ans, 0)