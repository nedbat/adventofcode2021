# https://adventofcode.com/2021/day/1

import collections

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
