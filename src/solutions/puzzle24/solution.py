import math
from sympy import symbols, linsolve, EmptySet


t = symbols('t', real=True)

class Particle():
    def __init__(self, input_line):        
        pos, vel = input_line.split("@")
        p = [int(x) for x in pos.split(",")]
        v = [int(x) for x in vel.split(",")]
        self.x = t*v[0] + p[0]
        self.y = t*v[1] + p[1]
        self.z = t*v[2] + p[2]

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
            x_intersect = linsolve([p1.x - p2.x], (t))
            if x_intersect == EmptySet:
                continue
            t_value = list(x_intersect)[0][0]
            x = float(p1.x.subs(t, t_value))
            y = float(p1.y.subs(t, t_value))
            pos = (x,y)
            if is_in_test_area(pos):
                pt1_ans += 1
    
    return (pt1_ans, 0)