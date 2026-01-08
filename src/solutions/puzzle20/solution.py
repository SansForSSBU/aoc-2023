from math import lcm
from copy import deepcopy
import pulp

class Pulse:
    def __init__(self, pulse, receiver, sender):
        self.pulse = pulse # True: high, False: low
        self.receiver = receiver
        self.sender = sender
    
    def invoke(self):
        global system
        if system.modules.get(self.receiver, None) is not None:
            system.modules[self.receiver].process_pulse(self)
        
        if self.receiver in system.specials.keys() and self.pulse == False:
            system.specials[self.receiver].append(system.presses)

class Module:
    def __init__(self, code, name, connections):
        self.type = code
        self.name = name
        self.outputs = connections
        if self.type == "%":
            self.state = False
        elif self.type == "&":
            self.inputs = {}

    def __str__(self):
        ret = f"{self.type}{self.name} -> {self.outputs}"
        if self.type == "&":
            ret = "INPUTS: " + str(self.inputs) + "\n" + ret
        return ret

    def send_bit(self, bit):
        global system
        for conn in self.outputs:
            system.pulse_queue.append(Pulse(bit, conn, self.name))

    def process_pulse(self, pulse):
        if self.type == "b":
            self.send_bit(pulse.pulse)

        if self.type == "%":
            if pulse.pulse == True:
                return
            self.state = not self.state
            self.send_bit(self.state)

        if self.type == "&":
            self.inputs[pulse.sender] = pulse.pulse
            all_pulses_high_pulses = list(self.inputs.values()).count(True) == len(self.inputs.values())
            output = not all_pulses_high_pulses
            self.send_bit(output)
    
    def get_upstreams(self):
        global system
        return system.get_upstreams(self.name)
        

class System():
    def __init__(self, modules):
        self.presses = 0
        self.modules = modules
        self.pulse_queue = []
        self.specials = {
            "xc": [],
            "th": [],
            "pd": [],
            "bp": []
        }
    
    def press_button(self):
        self.presses += 1
        highs = 0
        lows = 0
        self.pulse_queue.append(Pulse(False, "broadcaster", "button"))
        while len(system.pulse_queue) > 0:
            pulse = system.pulse_queue.pop()
            if pulse.pulse == True:
                highs += 1
            elif pulse.pulse == False:
                lows += 1
            else:
                raise ValueError()
            pulse.invoke()
        return highs,lows
    
    def send_pulse(self, module_name, pulse):
        module = [m for m in self.modules if m.name == module_name][0]
        module.process_pulse(pulse)

    def get_upstreams(self, module_name):
        return [module.name for module in system.modules.values() if module_name in module.outputs]

def solve_pt1():
    global system
    highs = 0
    lows = 0
    for i in range(1000):
        h,l = system.press_button()
        highs += h
        lows += l
    return highs*lows

def check_n2(n):
    if n % 3847 != 0:
        return False
    if (n+66) % 3906 != 0:
        return False
    return True

def check_n3(n):
    if n % 3847 != 0:
        return False
    if (n+66) % 3906 != 0:
        return False
    if (n+3440) % 3658 != 0:
        return False
    return True

def check_n4(n):
    if n % 3847 != 0:
        return False
    if (n+66) % 3906 != 0:
        return False
    if (n+3440) % 3658 != 0:
        return False
    if (n+3278) % 3550 != 0:
        return False
    return True

def solve_pt2():
    global system
    while True:
        system.press_button()
        if system.presses == 100000:
            break
    
    things = list(system.specials.values())
    reqs = []
    for sublist in things:
        delta = sublist[2] - sublist[1]
        yint = sublist[0] % delta
        for item in sublist:
            if (item-yint) % delta != 0:
                raise Exception()
        reqs.append((yint, delta))
    pass
    problem = pulp.LpProblem("find_n", pulp.LpMinimize)
    n = pulp.LpVariable("n", lowBound=1, cat="Integer")
    a = pulp.LpVariable("a", lowBound=1, cat="Integer")
    b = pulp.LpVariable("b", lowBound=1, cat="Integer")
    c = pulp.LpVariable("c", lowBound=1, cat="Integer")
    d = pulp.LpVariable("d", lowBound=1, cat="Integer")

    lp_vars = [a,b,c,d]
    problem += n
    for idx, req in enumerate(reqs):
        (yint, delta) = req
        problem += n - yint == lp_vars[idx] * delta
    problem.solve()
    return int(pulp.value(n))

def parse_input(input_file):
    modules = {}
    lines = input_file.split("\n")[:-1]
    for line in lines:
        e = line.split(" -> ")
        module_connections = e[1].split(", ")
        module_type = None
        module_name = None
        if e[0] == "broadcaster":
            module_type = "b"
            module_name = "broadcaster"
        else:
            module_type = e[0][0]
            module_name = e[0][1:]
        module = Module(module_type, module_name, module_connections)
        modules[module_name] = (module)

    for mod1 in modules.values():
        if mod1.type == "&":
            for mod2 in modules.values():
                if mod1.name in mod2.outputs:
                    mod1.inputs[mod2.name] = False

    system = System(modules)
    return system

system = None
def main(input_file):
    global system
    system = parse_input(input_file)
    system_clone = deepcopy(system)
    pt1_ans = solve_pt1()
    system = system_clone
    pt2_ans = solve_pt2()
    
    return (pt1_ans,pt2_ans)