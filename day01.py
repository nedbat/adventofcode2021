# https://adventofcode.com/2021/day/1

import collections
import itertools

with open("day01_input.txt") as f:
    depths = list(map(int, f))

increases = sum(b > a for a, b in zip(depths, depths[1:]))
print(f"Part 1: there are {increases} increases")

def sliding(seq, width):
    window = collections.deque()
    nums = iter(seq)
    total = 0
    # fill the window
    for _ in range(width):
        num = next(nums)
        total += num
        window.append(num)
    yield total

    for num in nums:
        bye = window.popleft()
        total += num - bye
        window.append(num)
        yield total

windows = list(sliding(depths, 3))
increases = sum(b > a for a, b in zip(windows, windows[1:]))
print(f"Part 2: there are {increases} increases")

# I don't like needing a list to count the increases, so:

def increases(seq):
    s1, s2 = itertools.tee(seq)
    next(s2)
    return sum(b > a for a, b in zip(s1, s2))

print(f"part 1: {increases(depths)}")
print(f"part 2: {increases(sliding(depths, 3))}")
