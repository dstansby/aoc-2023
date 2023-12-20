from lib import read_file

from dataclasses import dataclass
from typing import Literal
from collections import deque

@dataclass
class Pulse:
    val: Literal["low", "high"]
    dest: str

    def with_dest(self, dest: str) -> "Pulse":
        return type(self)(self.val, dest)

@dataclass
class Module:
    mod_type: str
    dests: list[str]

    def process(self, pulse: Pulse) -> list[Pulse]:
        # Process a pulse
        #
        # Returns list of mappings from destination to pulse
        ret = []
        if self.mod_type == "":
            for d in self.dests:
                ret.append(pulse.with_dest(d))

        return ret

if __name__ == "__main__":
    # I/O
    lines = read_file("20_example.txt")
    modules = {}
    for l in lines:
        name, dest = l.split(" -> ")
        module_type = ""
        if not name[0].isalpha():
            module_type = name[0]
            name = name[1:]

        modules[name] = Module(module_type, dest.split(", "))

    pulse_queue: deque[Pulse] = deque()
    # Press the button!
    pulse_queue.append(Pulse("low", "broadcaster"))

    while True:
        pulse = pulse_queue.popleft()
        new_pulses = modules[pulse.dest].process(pulse)
        for p in new_pulses:
            pulse_queue.append(p)

        break

    print(pulse_queue)
