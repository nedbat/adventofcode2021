# https://adventofcode.com/2021/day/5

import collections
import itertools
import re

TEST = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def read_lines(lines):
    for line in lines:
        x1, y1, x2, y2 = map(int, re.findall(r"\d+", line))
        yield x1, y1, x2, y2

def print_lines(counts):
    for y in range(10):
        for x in range(10):
            v = counts.get((x, y), 0)
            if v == 0:
                c = "."
            else:
                c = str(v)
            print(c, end="")
        print()

def direction(a, b):
    if a == b:
        return 0
    return (b - a) / abs(b - a)

def count_lines(lines, only_ortho):
    counts = collections.Counter()
    for x1, y1, x2, y2 in read_lines(lines):
        #print(f"adding {x1,y1,x2,y2}")
        dx = direction(x1, x2)
        dy = direction(y1, y2)
        if only_ortho:
            if dx != 0 and dy != 0:
                continue
        x, y = x1, y1
        counts[(x, y)] += 1
        while (x, y) != (x2, y2):
            x += dx
            y += dy
            counts[(x, y)] += 1
        #print_lines(counts)

    return counts

def part1(lines):
    counts = count_lines(lines, only_ortho=True)
    return sum(1 for v in counts.values() if v > 1)

def test_part1():
    assert part1(TEST.splitlines()) == 5

if __name__ == "__main__":
    with open("day05_input.txt") as f:
        ans = part1(f)
    print(f"part 1: {ans}")

def part2(lines):
    counts = count_lines(lines, only_ortho=False)
    return sum(1 for v in counts.values() if v > 1)

def test_part2():
    assert part2(TEST.splitlines()) == 12

if __name__ == "__main__":
    with open("day05_input.txt") as f:
        ans = part2(f)
    print(f"part 2: {ans}")


# Code from part 1 that I didn't need after refactoring from part 2:
#
# def fix_order(a, b):
#     if b < a:
#         a, b = b, a
#     return a, b
# 
# def range2d(x1, y1, x2, y2):
#     yield from itertools.product(range(x1, x2), range(y1, y2))

# def count_ortho_lines(lines):
#     counts = collections.Counter()
#     for x1, y1, x2, y2 in read_lines(lines):
#         if x1 == x2 or y1 == y2:
#             #print(f"adding {x1,y1,x2,y2}")
#             x1, x2 = fix_order(x1, x2)
#             y1, y2 = fix_order(y1, y2)
#             for x, y in range2d(x1, y1, x2+1, y2+1):
#                 counts[(x, y)] += 1
#             #print_lines(counts)
# 
#     return counts

