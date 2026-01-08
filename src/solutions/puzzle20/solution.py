from math import lcm

class Pulse:
    def __init__(self, pulse, receiver, sender):
        self.pulse = pulse
        self.receiver = receiver
        self.sender = sender
    
    def invoke(self):
        global system
        if system.modules.get(self.receiver, None) is not None:
            system.modules[self.receiver].process_pulse(self)

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

class System():
    def __init__(self, modules):
        self.modules = modules
        self.pulse_queue = []
    
    def press_button(self):
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

def solve_pt1():
    global system
    highs = 0
    lows = 0
    for i in range(1000):
        h,l = system.press_button()
        highs += h
        lows += l
    return highs*lows

def solve_pt2():
    button_presses = 0
    return button_presses

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
    pt1_ans = solve_pt1()
    pt2_ans = solve_pt2()
    
    return (pt1_ans,pt2_ans)