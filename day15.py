# https://adventofcode.com/2021/day/15

from pathlib import Path

import astar

def read_cave(fname):
    return [[int(c) for c in line.strip()] for line in Path(fname).open()]

def run_cave(cave):
    risks = {(0, 0): 0}
    w = len(cave[0])
    h = len(cave)
    maxrisk = 10 * (w + h)
    for depth in range(1, w + h):
        for x in range(depth + 1):
            y = depth - x
            if x >= w or y >= h:
                continue
            leftrisk = risks.get((x - 1, y), maxrisk)
            uprisk = risks.get((x, y - 1), maxrisk)
            risks[(x, y)] = min(uprisk, leftrisk) + cave[y][x]
    return risks[(w - 1), (h - 1)]

def part1(fname):
    return run_cave(read_cave(fname))

def test_part1():
    assert part1("day15_sample.txt") == 40

if __name__ == "__main__":
    ans = part1("day15_input.txt")
    print(f"part 1: {ans}")


def expand_cave(cave, n):
    w = len(cave[0])
    h = len(cave)
    lcave = [[0] * w * n for _ in range(h * n)]
    for mx in range(n):
        for my in range(n):
            depth = mx + my
            for x in range(w):
                for y in range(h):
                    r = ((cave[y][x] + depth) - 1) % 9 + 1
                    lcave[my * h + y][mx * w + x] = r
    return lcave

if 0:
    lcave = expand_cave(read_cave("day15_sample.txt"), 5)
    assert len(lcave) == 50
    assert len(lcave[0]) == 50
    for y in range(50):
        for x in range(50):
            print(lcave[y][x], end="")
        print()

def part2(fname):
    return run_cave(expand_cave(read_cave(fname), 5))

def test_part2():
    assert part2("day15_sample.txt") == 315

if __name__ == "__main__":
    ans = part2("day15_input.txt")
    print(f"part 2: {ans}")


class CaveState(astar.State):
    def __init__(self, cave, x, y):
        self.cave = cave
        self.maxx = len(self.cave[0]) - 1
        self.maxy = len(self.cave) - 1
        self.x = x
        self.y = y

    @classmethod
    def first(cls, cave):
        return cls(cave, 0, 0)

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def is_goal(self):
        return (self.x == self.maxx) and (self.y == self.maxy)

    def next_state(self, x, y, cost):
        return (
            self.__class__(self.cave, x, y),
            cost + self.cave[y][x]
        )

    def next_states(self, cost):
        if self.x > 0:
            yield self.next_state(self.x - 1, self.y, cost)
        if self.y > 0:
            yield self.next_state(self.x, self.y - 1, cost)
        if self.x < self.maxx:
            yield self.next_state(self.x + 1, self.y, cost)
        if self.y < self.maxy:
            yield self.next_state(self.x, self.y + 1, cost)

    def guess_completion_cost(self):
        # The remaining cost guess is 1 for each step left.
        return (self.maxx - self.x) + (self.maxy - self.y)

    def summary(self):
        return f"({self.x}, {self.y})"

def part1a(fname):
    cave = read_cave(fname) 
    cost = astar.search(CaveState.first(cave))
    return cost

def test_part1a():
    assert part1a("day15_sample.txt") == 40

if __name__ == "__main__":
    ans = part1a("day15_input.txt")
    print(f"part 1: {ans}")

def part2a(fname):
    cave = read_cave(fname) 
    cave = expand_cave(cave, 5)
    cost = astar.search(CaveState.first(cave))
    return cost

def test_part2a():
    assert part2a("day15_sample.txt") == 315

if __name__ == "__main__":
    ans = part2a("day15_input.txt")
    print(f"part 2: {ans}")

# What happened here: I started with A*, but I was using the full path as the
# state, and it was taking forever.  So I changed to the diagonal march, but
# assumed paths would only go down and right.  This works for part 1, and for
# the sample data for both parts, but doesn't work for the input data for part
# 2.
#
# So I went back to A*, using only x,y as the state, and it worked :)
