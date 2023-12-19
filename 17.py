from lib import read_arr

import numpy as np

from dataclasses import dataclass
from collections import deque
from copy import copy

from typing import Literal

from functools import cache

Step = Literal["U", "D", "L", "R"]


class Index(tuple[int, int]):
    def __add__(self, other) -> "Index":
        return type(self)((self[0] + other[0], self[1] + other[1]))


@dataclass
class StepChain:
    idx: tuple[int, int]
    previous_steps: str
    total: int

steps = {
    "R": Index((0, 1)),
    "L": Index((0, -1)),
    "U": Index((-1, 0)),
    "D": Index((1, 0))
}

def out_of_bounds(arr, idx) -> bool:
    return any(i < 0 for i in idx) or idx[0] >= arr.shape[0] or idx[1] >= arr.shape[1]

@profile
def min_length(arr, min_steps: int, max_steps: int) -> StepChain:
    idx = Index((0, 0))
    chains: deque[StepChain] = deque()
    chains.append(StepChain(idx, "R", 0))
    chains.append(StepChain(idx, "D", 0))

    best_chain = StepChain(idx, "", 1_000_000)

    seen = dict()

    final_idx = Index(np.array(arr.shape) - 1)
    next_steps_dict = {
        "R": ["U", "D"],
        "L": ["U", "D"],
        "U": ["R", "L"],
        "D": ["R", "L"]
    }
    counter = 0

    while len(chains):
        chain = chains.popleft()

        last_step = chain.previous_steps[-1]
        next_steps = next_steps_dict[last_step]

        for next_step in next_steps:
            new_tot = chain.total
            
            for n_steps in range(1, max_steps + 1):
                next_idx = Index(
                    (
                        chain.idx[0] + steps[next_step][0] * n_steps,
                        chain.idx[1] + steps[next_step][1] * n_steps,
                     )
                )
                try:
                    new_tot += arr[next_idx[0], next_idx[1]]
                except IndexError:
                    # Further steps will be out of bounds
                    break

                if n_steps < min_steps:
                    continue

                if next_idx[0] < 0 or next_idx[1] < 0:
                    # Further steps will be out
                    continue
                
                if next_idx == final_idx:
                    if new_tot < best_chain.total:
                        best_chain = StepChain(next_idx, chain.previous_steps + next_step * n_steps, new_tot)
                    # Rest will be out of bounds so just break
                    break
                
                # If we've taken this step before, and the cost was lower than our current cost
                if seen.get((chain.idx, next_idx), 1_000_000) <= new_tot:
                    continue
        
                
                chains.append(StepChain(next_idx, chain.previous_steps + next_step * n_steps, new_tot))
                seen[(chain.idx, next_idx)] = new_tot
                next_idx = next_idx + steps[next_step]

        counter += 1
        if counter % 10000 == 0:
            print(len(chains))

    return best_chain


if __name__ == "__main__":
    arr = read_arr("17_example.txt", dtype=int)
    print(min_length(arr, 1, 3))
    print(min_length(arr, 4, 10))
