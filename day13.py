# https://adventofcode.com/2021/day/13

import re

from pathlib import Path

def read_paper(fname):
    dots = set()
    folds = []
    for line in Path(fname).open():
        if m := re.match(r"(\d+),(\d+)", line):
            dots.add(tuple(map(int, m.groups())))
        elif m := re.match(r"fold along (.)=(\d+)", line):
            folds.append((m[1], int(m[2])))
    return dots, folds

def fold(dots, axis, where):
    folded = set()
    for x, y in dots:
        if axis == "x" and x > where:
            x = where - (x - where)
        elif axis == "y" and y > where:
            y = where - (y - where)
        folded.add((x, y))
    return folded

def test_fold():
    dots, folds = read_paper("day13_sample.txt")
    folded = fold(dots, *folds[0])
    assert len(folded) == 17

if __name__ == "__main__":
    dots, folds = read_paper("day13_input.txt")
    folded = fold(dots, *folds[0])
    print(f"part 1: {len(folded)} dots visible after one fold")
