from math import lcm

lines = []
with open("puzzle20/input.txt") as input:
    lines = input.read().split("\n")

def send_pulse(module_name, pulse):
    module = [m for m in modules if m.name == module_name][0]
    module.process_pulse(pulse)

rx_invoked = False

modules = {}
pulse_queue = []
class Pulse:
    def __init__(self, pulse, receiver, sender):
        self.pulse = pulse
        self.receiver = receiver
        self.sender = sender
    
    def invoke(self):
        global rx_invoked
        if modules.get(self.receiver, None) is not None:
            modules[self.receiver].process_pulse(self)
        else:
            if self.receiver == "rx":
                if self.pulse == False:
                    rx_invoked = True
            pass # Good place for a break... point.


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
        for conn in self.outputs:
            pulse_queue.append(Pulse(bit, conn, self.name))

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

def press_button():
    highs = 0
    lows = 0
    pulse_queue.append(Pulse(False, "broadcaster", "button"))
    while len(pulse_queue) > 0:
        pulse = pulse_queue.pop()
        if pulse.pulse == True:
            highs += 1
        elif pulse.pulse == False:
            lows += 1
        else:
            print("pulse.pulse is not high or low?!")
        pulse.invoke()
        pass

    return highs,lows

def solve_pt1():
    highs = 0
    lows = 0
    for i in range(1000):
        h,l = press_button()
        highs += h
        lows += l
    return highs*lows

def solve_pt2():
    button_presses = 0
    occs = {}
    for k in modules["kh"].inputs.keys():
        occs[k] = []
    while True:
        press_button()
        button_presses += 1
        if rx_invoked:
            break
        for k, v in modules["kh"].inputs.items():
            l = occs[k]
            if v == True:
                if len(l) == 0 or type(l[-1]) is not int:
                    l.append(button_presses)
            else:
                if len(l) != 0 and type(l[-1]) is int:
                    l[-1] = range(l[-1], button_presses)
                    pass
        
        if min([len(o) for o in occs.values()]) >= 5:
            cycles = []
            for k in occs.keys():
                ex1 = occs[k][2]
                ex2 = occs[k][3]
                on_time = len(ex1)
                off_time = ex2[0] - ex1[0] - on_time
                cycles.append((off_time, off_time+on_time))
                pass
            """
            n = 0
            jump = 0
            success = False
            while not success:
                n += jump
                success = True
                for c in cycles:
                    if not n % c[1] >= c[0]:
                        success = False
                        jump = (2048 - n%3906)
                        #jump = max(c[0] - (n % c[1]), jump)
                pass
            """
            cycles = [f"N % {c[1]} >= {c[0]}" for c in cycles]
            return cycles

    return button_presses


#print("Part 1:", solve_pt1())
#print("Part 2:", solve_pt2())
p2_ans = solve_pt2()
for l in p2_ans:
    print(l)