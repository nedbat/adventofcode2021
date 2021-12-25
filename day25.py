# https://adventofcode.com/2021/day/25
# Sea Cucumber

import itertools
from pathlib import Path

import numpy as np

from helpers import timeit

def read_floor(fname):
    return np.array([[".>v".find(c) for c in l.strip()] for l in Path(fname).open()])

def print_floor(floor):
    print()
    nrows, ncols = floor.shape
    for nr in range(nrows):
        for nc in range(ncols):
            print(".>v"[floor[nr,nc]], end="")
        print()

@timeit
def part1(fname):
    floor = read_floor(fname)
    for step_num in itertools.count(start=1):
        moving_east = (floor == 1) & (np.roll(floor, -1, 1) == 0)
        any_east = np.any(moving_east == True)
        if any_east:
            floor[moving_east == True] = 0
            floor[np.roll(moving_east, 1, 1)] = 1

        moving_south = (floor == 2) & (np.roll(floor, -1, 0) == 0)
        any_south = np.any(moving_south == True)
        if any_south:
            floor[moving_south == True] = 0
            floor[np.roll(moving_south, 1, 0)] = 2

        if not any_east and not any_south:
            return step_num

def test_part1():
    assert part1("day25_sample1.txt") == 58

if __name__ == "__main__":
    print(f"part 1: {part1('day25_input.txt')}")
