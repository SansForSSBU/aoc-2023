from copy import deepcopy

class Brick():
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "~".join([",".join([str(x) for x in self.pos1]), ",".join([str(x) for x in self.pos2])])

    def __init__(self, line):
        pos1, pos2 = line.split("~")
        self.pos1 = [int(x) for x in pos1.split(",")]
        self.pos2 = [int(x) for x in pos2.split(",")]
        self.recalculate_ranges()

    def recalculate_ranges(self):
        self.ranges = []
        for i, _ in enumerate(self.pos1):
            r = sorted([self.pos1[i], self.pos2[i]])
            r[1] = r[1] + 1
            self.ranges.append(range(r[0], r[1]))

    def fall_one(self):
        self.pos1[2] -= 1
        self.pos2[2] -= 1
        self.recalculate_ranges()

    def overlaps_xyz(self, other):
        return ranges_overlap(self.ranges[0], other.ranges[0]) and ranges_overlap(self.ranges[1], other.ranges[1]) and ranges_overlap(self.ranges[2], other.ranges[2])

    def overlaps_xy(self, other):
        return ranges_overlap(self.ranges[0], other.ranges[0]) and ranges_overlap(self.ranges[1], other.ranges[1])

def ranges_overlap(range1, range2):
    r1 = set(range1)
    r2 = set(range2)
    l = list(r1 & r2)
    return len(l) != 0

def solve_pt1(bricks):
    bricks = sorted(bricks, key=lambda brick: brick.pos1[2])
    landed = []
    supports = []
    for idx, brick in enumerate(bricks):
        possible_landed = [l for l in landed if brick.overlaps_xy(l)]
        while True:
            supported_by = []
            fallen_brick = deepcopy(brick)
            fallen_brick.fall_one()
            if brick.pos1[2] <= 0 or brick.pos2[2] <= 0:
                break
            for land in possible_landed:
                if land.overlaps_xyz(brick):
                    supported_by.append(land)
            if len(supported_by) > 0:
                break
            brick = fallen_brick
        landed.append(brick)
        supports.append([str(x) for x in supported_by])
        print(idx)
    c = set()
    str_landed = [str(brick) for brick in landed]
    for idx, s in enumerate(supports):
        supports[idx] = [str_landed.index(x) for x in s]
    supported_by = {k:v for k, v in enumerate(supports)}
    supports_others = {k: [] for k in supported_by.keys()}
    for k,v in supported_by.items():
        for a in v:
            supports_others[a].append(k)
    necessary_bricks = {k:v for k,v in supports_others.items() if len(v) > 0}
    definitely_necessary_bricks = {}
    rm = []
    for brick_id, supporting in necessary_bricks.items():
        for idx in supporting:
            if len(supported_by[idx]) == 1:
                definitely_necessary_bricks[brick_id] = supporting
                rm.append(brick_id)
    for r in list(set(rm)):
        del necessary_bricks[r]
    pass
    a = []
    for k,v in definitely_necessary_bricks.items():
        a.extend(v)
    a = list(set(a))
    for b in list(supported_by.keys()):
        if supported_by.get(b, []) == []:
            del supported_by[b]
    for b in a:
        if b in supported_by.keys():
            del supported_by[b]
    # account for ones which could be supported by something else
    # 334 too low?
    # 416 too low

def main(input_file):
    bricks = [Brick(b) for b in input_file.split("\n") if len(b) > 0]
    pt1_ans = solve_pt1(bricks)
    pass