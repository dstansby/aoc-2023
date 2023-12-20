from lib import read_file

from dataclasses import dataclass, field
from typing import Literal
from collections import deque
from abc import ABC, abstractmethod


PulseVal = Literal["low", "high"]
@dataclass
class Pulse:
    val: PulseVal
    source: str
    dest: str

    def __str__(self):
        return f"{self.source} -{self.val}-> {self.dest}"


@dataclass
class Module(ABC):
    name: str
    dests: list[str]

    @abstractmethod
    def process(self, pulse: Pulse) -> list[Pulse]:
        pass
    
class Broadcaster(Module):
    def process(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.val, self.name, d) for d in self.dests]
    

@dataclass
class FlipFlop(Module):
    state: bool = False

    def process(self, pulse: Pulse) -> list[Pulse]:
        if pulse.val == "high":
            return []
        else:
            self.state = not self.state
            if self.state:
                return [Pulse("high", self.name, d) for d in self.dests]
            else:
                return [Pulse("low", self.name, d) for d in self.dests]
            
@dataclass
class Conjunction(Module):
    prev_pulses: dict[str, PulseVal] = field(default_factory=dict)

    def process(self, pulse: Pulse) -> list[Pulse]:
        self.prev_pulses[pulse.source] = pulse.val
        if all(v == "high" for v in self.prev_pulses.values()):
            return [Pulse("low", self.name, d) for d in self.dests]
        else:
            return [Pulse("high", self.name, d) for d in self.dests]


if __name__ == "__main__":
    # I/O
    lines = read_file("20_example_2.txt")
    modules: dict[str, Module] = {}
    for l in lines:
        name, dest = l.split(" -> ")
        module_type = ""
        if not name[0].isalpha():
            module_type = name[0]
            name = name[1:]
        
        dests = dest.split(", ")

        if module_type == "":
            modules[name] = Broadcaster(name, dests)
        elif module_type == "%":
            modules[name] = FlipFlop(name, dests)
        elif module_type == "&":
            modules[name] = Conjunction(name, dests)

        else:
            assert False, module_type

    # Populate conjunction dicts
    for module in modules.values():
        for dest in module.dests:
            if isinstance((dest_mod :=modules[dest]), Conjunction):
                dest_mod.prev_pulses[module.name] = "low"


    pulse_queue: deque[Pulse] = deque()
    # Press the button!
    pulse_queue.append(Pulse("low", "button", "broadcaster"))

    while len(pulse_queue):
        pulse = pulse_queue.popleft()
        print(pulse)
        new_pulses = modules[pulse.dest].process(pulse)
        for p in new_pulses:
            pulse_queue.append(p)


    print(modules)
