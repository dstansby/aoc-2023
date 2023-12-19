from pathlib import Path

import numpy as np
import numpy.typing as npt

def read_file(fname: str) -> list[str]:
    with open(Path("inputs") / fname) as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    return lines


def read_arr(fname: str, dtype=str) -> npt.NDArray:
    lines = read_file(fname)

    arr = np.empty((len(lines), len(lines[0])), dtype=dtype)

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            arr[i, j] = char

    return arr
