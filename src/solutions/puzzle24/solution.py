import math

class Particle():
    def __init__(self, input_line):
        pos, vel = input_line.split("@")
        self.pos = [float(x) for x in pos.split(",")]
        self.vel = [float(x) for x in vel.split(",")]

    def pos_at_time(self, t):
        x = self.pos[0] + (self.vel[0] * t)
        y = self.pos[1] + (self.vel[1] * t)
        z = self.pos[2] + (self.vel[2] * t)
        return (x,y,z)


    def intersects_at(self, other):
        # Find at what t self.x = other.x
        spx = self.pos[0]
        opx = other.pos[0]
        svx = self.vel[0]
        ovx = other.vel[0]
        pos_diff = opx - spx # How much distance is there to cover?
        vel_diff = svx - ovx # How fast is self catching up to other?
        if vel_diff == 0:
            if pos_diff == 0:
                pass
            return None
        time = pos_diff / vel_diff
        if time < 0:
            return None
        
        self_at_time = self.pos_at_time(time)
        other_at_time = other.pos_at_time(time)
        if math.isclose(self_at_time[1], other_at_time[1], abs_tol=100):
            print(time)
            return self_at_time
        return None

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
            intersect = p1.intersects_at(p2)
            if intersect is None:
                continue
            if is_in_test_area(intersect):
                pt1_ans += 1
    return (pt1_ans, 0)
    # 1 wrong
    pass