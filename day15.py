# https://adventofcode.com/2021/day/15

from pathlib import Path

def read_cave(fname):
    return [[int(c) for c in line.strip()] for line in Path(fname).open()]

def run_cave(cave):
    risks = {(0, 0): 0}
    paths = {(0, 0): str(cave[0][0])}
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
            if uprisk < leftrisk:
                paths[(x, y)] = paths[(x, y - 1)] + str(cave[y][x])
            else:
                paths[(x, y)] = paths[(x - 1, y)] + str(cave[y][x])
    print(paths[(w-1), (h-1)])
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
