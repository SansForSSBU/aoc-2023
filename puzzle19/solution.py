lines = []
with open("puzzle19/input.txt") as input:
    lines = input.read().split("\n")

class Part():
    def __init__(self, line):
        self.attrs = dict([attr.split("=") for attr in line.strip("{}").split(",")])
        for key in self.attrs:
            self.attrs[key] = int(self.attrs[key])
        self.location = "in"

class Rule():
    def __init__(self, spec):
        operator_idx = max(spec.find("<"), spec.find(">"))
        if operator_idx == -1:
            self.sendto = spec
            return
        self.operator = spec[operator_idx]
        cond,self.sendto = spec.split(":")
        self.attr,self.value = cond.split(self.operator)
        self.value = int(self.value)
        pass

    def match(self, part):
        if not hasattr(self, "operator"):
            return True
        part_value = part.attrs[self.attr]
        if self.operator == '>':
            return part_value > self.value
        if self.operator == '<':
            return part_value < self.value


class Workflow():
    def __init__(self, line):
        l = line.strip("}").split("{")
        self.name = l[0]
        self.rules = [Rule(r) for r in l[1].split(",")]

    def move_part(self, part):
        for rule in self.rules:
            if rule.match(part):
                return rule.sendto


def solve_pt1():
    ans = 0
    while len(parts) > 0:
        part = parts.pop(0)
        workflow = [w for w in workflows if w.name == part.location][0]
        part.location = workflow.move_part(part)
        if part.location == "A":
            ans += sum(part.attrs.values())
            continue
        elif part.location == "R":
            continue
        parts.append(part)
    return ans
def solve_pt2():
    return 0

split = lines.index("")
workflows = [Workflow(l) for l in lines[:split]]
parts = [Part(l) for l in lines[split+1:]]
print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())