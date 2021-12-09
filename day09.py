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
            yield v, x, y

def part1(fname):
    hm = read_heightmap(fname)
    return sum(v + 1 for v, _, _ in low_points(hm))

def test_part1():
    assert part1("day09_sample.txt") == 15

if __name__ == "__main__":
    print(f"part 1: {part1('day09_input.txt')}")


from rich.console import Console

def print_heightmap(hm):
    con = Console(highlight=False)
    lps = {(x,y): v for v, x, y in low_points(hm)}
    for y, l in enumerate(hm):
        for x, c in enumerate(l):
            if c == 9:
                style = "bold"
            elif (x, y) in lps:
                assert lps[(x, y)] == c
                style = "red"
            else:
                style = ""
            if style:
                con.print(f"[{style}]{c}[/{style}]", end="")
            else:
                con.print(c, end="")
        con.print()
    con.print()

#print_heightmap(read_heightmap("day09_sample.txt"))

def explore_basin(hm, x, y):
    """Return the set of coordinates in the basin or lowpoint x, y"""
    h = len(hm)
    w = len(hm[0])
    to_explore = set([(x, y)])
    explored = set()
    while to_explore:
        ex, ey = to_explore.pop()
        explored.add((ex, ey))
        for ox, oy in neighbors(w, h, ex, ey):
            if (ox, oy) in to_explore:
                continue
            if (ox, oy) in explored:
                continue
            if hm[oy][ox] == 9:
                continue
            to_explore.add((ox, oy))
    return explored

def basins(hm):
    for v, x, y in low_points(hm):
        basin_points = explore_basin(hm, x, y)
        yield x, y, basin_points

def part2(fname):
    hm = read_heightmap(fname)
    basin_sizes = [len(bp) for _, _, bp in basins(hm)]
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

def test_part2():
    assert part2("day09_sample.txt") == 1134

if __name__ == "__main__":
    print(f"part 2: {part2('day09_input.txt')}")
