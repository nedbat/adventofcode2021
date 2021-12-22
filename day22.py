# https://adventofcode.com/2021/day/22
# Reactor Reboot

import itertools
import re
from pathlib import Path

import pytest

def read_steps(fname):
    for line in Path(fname).open():
        op, _, xyz = line.partition(" ")
        xyznums = map(int, re.findall(r"-?\d+", xyz))
        yield [op, *xyznums]

def clip_range(lo, hi, minlo, maxhi):
    hi += 1
    maxhi += 1
    return range(max(lo, minlo), min(hi, maxhi))

@pytest.mark.parametrize("lo, hi, nums", [
    (-1, 2, [-1, 0, 1, 2]),
    (-5, 2, [-3, -2, -1, 0, 1, 2]),
    (1, 5, [1, 2, 3]),
    (-10, -5, []),
])
def test_clip_range(lo, hi, nums):
    assert list(clip_range(lo, hi, -3, 3)) == nums

def part1(fname):
    cubes = set()
    for op, xl, xh, yl, yh, zl, zh in read_steps(fname):
        xr = clip_range(xl, xh, -50, 50)
        yr = clip_range(yl, yh, -50, 50)
        zr = clip_range(zl, zh, -50, 50)
        for xyz in itertools.product(xr, yr, zr):
            if op == "on":
                cubes.add(xyz)
            elif xyz in cubes:
                cubes.remove(xyz)
    return len(cubes)

def test_part1():
    assert part1("day22_sample.txt") == 590784

if __name__ == "__main__":
    print(f"part 1: {part1('day22_input.txt')}")
