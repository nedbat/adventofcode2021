# https://adventofcode.com/2021/day/9

import itertools
from pathlib import Path

def read_heightmap(fname):
    text = Path(fname).read_text()
    heightmap = [[int(c) for c in l] for l in text.splitlines()]
    return heightmap

def range2d(endx, endy):
    yield from itertools.product(range(endx), range(endy))

def neighbors(w, h, x, y):
    if x > 0:
        yield (x - 1, y)
    if x < w - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < h - 1:
        yield (x, y + 1)

def low_points(hm):
    h = len(hm)
    w = len(hm[0])
    for x, y in range2d(w, h):
        v = hm[y][x]
        if all(v < hm[oy][ox] for ox, oy in neighbors(w, h, x, y)):
            yield v

def part1(fname):
    hm = read_heightmap(fname)
    return sum(lp + 1 for lp in low_points(hm))

def test_part1():
    assert part1("day09_sample.txt") == 15

if __name__ == "__main__":
    print(f"part 1: {part1('day09_input.txt')}")
