import copy
lines = []
with open("puzzle19/input.txt") as input:
    lines = input.read().split("\n")

class Part():
    def __init__(self, line):
        self.attrs = dict([attr.split("=") for attr in line.strip("{}").split(",")])
        for key in self.attrs:
            self.attrs[key] = int(self.attrs[key])
        self.location = "in"

    def __str__(self):
        return f"{self.location} {self.attrs}"

    
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
    
    def __str__(self):
        if hasattr(self, "operator"):
            return f"{self.attr}{self.operator}{self.value} {self.sendto}"
        else:  
            return f"{self.sendto}"

    def match(self, part):
        if not hasattr(self, "operator"):
            return True
        part_value = part.attrs[self.attr]
        if self.operator == '>':
            return part_value > self.value
        if self.operator == '<':
            return part_value < self.value
    
    def next_parts(self, part):
        if not hasattr(self, "operator"):
            state = copy.deepcopy(part)
            state.location = self.sendto
            return [state]
        
        curr_range = part.attrs[self.attr]
        next_states = []
        if self.operator == '>':
            accept_start = max(curr_range[0], self.value+1)
            reject_end = min(curr_range[-1], self.value)
            if accept_start in curr_range:
                # Accept
                state = copy.deepcopy(part)
                state.attrs[self.attr] = range(accept_start, curr_range[-1]+1)
                state.location = self.sendto
                next_states.append(state)
                pass
            if reject_end in curr_range:
                # Reject
                state = copy.deepcopy(part)
                state.attrs[self.attr] = range(curr_range[0], reject_end+1)
                next_states.append(state)
                pass
        if self.operator == '<':
            accept_start = min(curr_range[-1], self.value-1)
            reject_end = max(curr_range[0], self.value)
            if accept_start in curr_range:
                # Accept
                state = copy.deepcopy(part)
                state.attrs[self.attr] = range(accept_start, curr_range[-1]+1)
                state.location = self.sendto
                next_states.append(state)
                pass
            if reject_end in curr_range:
                # Reject
                state = copy.deepcopy(part)
                state.attrs[self.attr] = range(curr_range[0], reject_end+1)
                next_states.append(state)
                pass
        return next_states
    
        


class Workflow():
    def __init__(self, line):
        l = line.strip("}").split("{")
        self.name = l[0]
        self.rules = [Rule(r) for r in l[1].split(",")]

    def __str__(self):
        string = self.name + ":"
        for rule in self.rules:
            string = string + " " + str(rule) + ";"
        return string
    
    def move_part(self, part):
        for rule in self.rules:
            if rule.match(part):
                return rule.sendto
    
    def possible_next_states(self, part):
        states = []
        p = [part]
        for rule in self.rules:
            next_parts = []
            for part in p:
                new_parts = rule.next_parts(part)
                while len(new_parts) > 0:
                    part = new_parts.pop(0)
                    if part.location != self.name:
                        states.append(part)
                    else:
                        next_parts.append(part)
                pass
            p = next_parts
        return states

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
    parts = [Part(lines[split+1])]
    for attr in parts[0].attrs.keys():
        parts[0].attrs[attr] = range(1, 4001)

    ends = []
    rejects = []
    while len(parts) > 0:
        part = parts.pop(0)
        workflow = [w for w in workflows if w.name == part.location][0]
        next_states = workflow.possible_next_states(part)
        print("Part: ", part)
        print("Workflow: ", workflow)
        print("Next states: ")
        for s in next_states:
            print(s)
            pass
            if s.location == "A":
                ends.append(s)
            elif s.location == "R":
                rejects.append(s)
            else:
                parts.append(s)
        pass
    accepts = 0
    for end in ends + rejects:
        n = 1
        for attr in end.attrs.values():
            n = n * len(attr)
        accepts += n
    print(accepts)
    print(len(range(1,4001))*len(range(1,4001))*len(range(1,4001))*len(range(1,4001)))
    return accepts

split = lines.index("")
workflows = [Workflow(l) for l in lines[:split]]
parts = [Part(l) for l in lines[split+1:]]
print("Part 1:", solve_pt1())
print("Part 2:", solve_pt2())