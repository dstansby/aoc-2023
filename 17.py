from lib import read_arr

import numpy as np

from dataclasses import dataclass
from collections import deque
from copy import copy

from typing import Literal

Step = Literal["U", "D", "L", "R"]


class Index(tuple[int, int]):
    def __add__(self, other) -> "Index":
        return type(self)((self[0] + other[0], self[1] + other[1]))


@dataclass
class StepChain:
    idx: Index
    previous_steps: str
    total: int

steps = {
    "R": Index((0, 1)),
    "L": Index((0, -1)),
    "U": Index((-1, 0)),
    "D": Index((1, 0))
}

@profile
def min_length(arr, min_steps: int, max_steps: int) -> StepChain:
    idx = Index((0, 0))
    chains: deque[StepChain] = deque()
    chains.append(StepChain(idx, "R", 0))
    chains.append(StepChain(idx, "D", 0))

    best_chain = StepChain(idx, "", 1_000_000)
    best_chains = []

    seen = dict()

    final_idx = Index(np.array(arr.shape) - 1)
    next_steps_dict = {
        "R": ["U", "D"],
        "L": ["U", "D"],
        "U": ["L", "R"],
        "D": ["L", "R"]
    }
    counter = 0

    while len(chains):
        chain = chains.popleft()

        # Loop through L/R or U/D
        for next_step in next_steps_dict[chain.previous_steps[-1]]:
            new_tot = chain.total
            next_idx = chain.idx
            
            for n_steps in range(1, max_steps + 1):
                # Take one more step
                next_idx += steps[next_step]
                
            
                if next_idx[0] < 0 or next_idx[1] < 0:
                    # Further steps will be out of bounds
                    break

                # Update total
                try:
                    new_tot += arr[next_idx[0], next_idx[1]]
                except IndexError:
                    # Further steps will be out of bounds
                    break

                if n_steps < min_steps:
                    # Go to next number of steps,
                    # having accumulated the total on this step
                    continue

                # If we've taken this step before, and the cost was lower than our current cost
                if seen.get(((next_idx, next_step)), 1_000_000) <= new_tot:
                    continue
                
                if next_idx == final_idx:
                    # At the end
                    if new_tot < best_chain.total:
                        best_chain = StepChain(next_idx, chain.previous_steps + next_step * n_steps, new_tot)
                        best_chains.append(best_chain)
                    # Rest will be out of bounds so just break
                    break

                chains.append(StepChain(next_idx, chain.previous_steps + next_step * n_steps, new_tot))
                seen[(next_idx, next_step)] = new_tot

        counter += 1
        if counter % 2**12 == 0:
            print(len(chains))

    return best_chain


if __name__ == "__main__":
    arr = read_arr("17_input.txt", dtype=int)
    # print(min_length(arr, 1, 3))
    print(min_length(arr, 4, 10))
