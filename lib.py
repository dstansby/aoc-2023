from pathlib import Path

def read_file(fname: str) -> list[str]:
    with open(Path("inputs") / fname) as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    return lines
