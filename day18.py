# https://adventofcode.com/2021/day/18

import ast
import copy
import math
from pathlib import Path

import pytest

class SfNum:
    def __init__(self, nums):
        self.nums = copy.deepcopy(nums)

    @classmethod
    def from_text(cls, text):
        return cls(ast.literal_eval(text))
    
    def __str__(self):
        return str(self.nums)

    def copy(self):
        return SfNum(self.nums)

    def walk(self):
        """Walk from left to right, yielding idx, kind, value."""
        yield from self._walk((), self.nums)

    def _walk(self, idx, nums):
        if isinstance(nums, int):
            yield "num", idx, nums
        else:
            yield "pair", idx, nums
            yield from self._walk(idx + (0,), nums[0])
            yield from self._walk(idx + (1,), nums[1])

    def __getitem__(self, idx):
        val = self.nums
        for i in idx:
            val = val[i]
        return val

    def __setitem__(self, idx, val):
        nums = self.nums
        for i in idx[:-1]:
            nums = nums[i]
        nums[idx[-1]] = val

    def reduce(self):
        while True:
            # Find a pair to explode:
            happened = False
            left_num = left_num_idx = add_to_right = explode_idx = None
            walking = self.walk()
            for kind, idx, val in walking:
                if kind == "num":
                    left_num = val
                    left_num_idx = idx
                elif len(idx) == 4:
                    # This is the pair to explode 
                    if left_num_idx is not None:
                        self[left_num_idx] = left_num + val[0]
                    add_to_right = val[1]
                    explode_idx = idx
                    happened = True
                    break
            if happened:
                # skip the two numbers in the exploded pair
                next(walking); next(walking)
                for kind, idx, val in walking:
                    if kind == "num":
                        self[idx] = val + add_to_right
                        break
            if happened:
                self[explode_idx] = 0
                continue

            # Find a number to split:
            happened = False
            for kind, idx, val in self.walk():
                if kind == "num" and val >= 10:
                    self[idx] = [math.floor(val / 2), math.ceil(val / 2)]
                    happened = True
                    break
            if not happened:
                break

    def __add__(self, other):
        added = SfNum([self.nums, other.nums])
        added.reduce()
        return added

    def magnitude(self):
        return magnitude(self.nums)

def read_sfnums(fname):
    yield from map(SfNum.from_text, Path(fname).open())

def test_add():
    sf1 = SfNum([[[[4,3],4],4],[7,[[8,4],9]]])
    sf2 = SfNum([1,1])
    assert (sf1 + sf2).nums == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

def magnitude(sfnum):
    if isinstance(sfnum, int):
        return sfnum
    else:
        return magnitude(sfnum[0]) * 3 + magnitude(sfnum[1]) * 2

@pytest.mark.parametrize("nums, mag", [
    ([[1,2],[[3,4],5]], 143),
    ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
    ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
    ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
    ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
    ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
])
def test_magnitude(nums, mag):
    assert magnitude(nums) == mag

def part1(fname):
    sfnums = read_sfnums(fname)
    sfnum = next(sfnums)
    for sfnum_next in sfnums:
        sfnum = sfnum + sfnum_next
    return sfnum.magnitude()

def test_part1():
    assert part1("day18_sample1.txt") == 4140

if __name__ == "__main__":
    print(f"part 1: {part1('day18_input.txt')}")
