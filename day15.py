# https://adventofcode.com/2021/day/15

from pathlib import Path

def read_cave(fname):
    return [[int(c) for c in line.strip()] for line in Path(fname).open()]

def part1(fname):
    cave = read_cave(fname)
    risk = astar.search(CaveState.first(cave), log=5)
    return risk

def part1(fname):
    cave = read_cave(fname)
    risks = {(0, 0): (0, [])}
    w = len(cave[0])
    h = len(cave)
    for depth in range(1, w + h):
        for x in range(depth + 1):
            y = depth - x
            if x >= w or y >= h:
                continue
            leftrisk = risks.get((x - 1, y))
            uprisk = risks.get((x, y - 1))
            if leftrisk is None:
                takeup = True
            elif uprisk is None:
                takeup = False
            else:
                takeup = (uprisk[0] < leftrisk[0])
            if takeup:
                risks[(x, y)] = uprisk[0] + cave[y][x], uprisk[1] + [(x, y)]
            else:
                risks[(x, y)] = leftrisk[0] + cave[y][x], leftrisk[1] + [(x, y)]
    return risks[(w - 1), (h - 1)][0]

def test_part1():
    assert part1("day15_sample.txt") == 40

if __name__ == "__main__":
    ans = part1("day15_input.txt")
    print(f"part 1: {ans}")
