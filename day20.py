# https://adventofcode.com/2021/day/20

import itertools
from pathlib import Path

N5 = list(itertools.product(range(-2, 3), repeat=2))

class Image:
    def __init__(self, pts, darkbg):
        # darkbg: True means the bg is dark, and pts are light pixels
        self.pts = pts
        self.darkbg = darkbg

    def census(self):
        assert self.darkbg
        return len(self.pts)

    def bounds(self):
        minx = min(x for x, y in self.pts)
        maxx = max(x for x, y in self.pts)
        miny = min(y for x, y in self.pts)
        maxy = max(y for x, y in self.pts)
        return minx, maxx, miny, maxy

    def neighborhood_as_number(self, x, y):
        num = 0
        for p, (dy, dx) in enumerate(itertools.product([1, 0, -1], repeat=2)):
            if ((x + dx, y + dy) in self.pts) == self.darkbg:
                num += 2 ** p
        return num

    def enhance(self, algorithm):
        minx, maxx, miny, maxy = self.bounds()
        npts = set()
        ndarkbg = (0 in algorithm) != self.darkbg
        for x in range(minx - 2, maxx + 3):
            for y in range(miny - 2, maxx + 3):
                xynum = self.neighborhood_as_number(x, y)
                if (xynum in algorithm) == ndarkbg:
                    npts.add((x, y))
        return Image(npts, ndarkbg)

    def enhance_slower(self, algorithm):
        # This seemed like a better way: consider each lit point, rather than
        # every point in the grid, but it's 50% slower?
        considered = set()
        npts = set()
        ndarkbg = (0 in algorithm) != self.darkbg
        for x, y in self.pts:
            for dx, dy in N5:
                nx = x + dx
                ny = y + dy
                if (nx, ny) not in considered:
                    xynum = self.neighborhood_as_number(nx, ny)
                    if (xynum in algorithm) == ndarkbg:
                        npts.add((nx, ny))
                    considered.add((nx, ny))
        return Image(npts, ndarkbg)

def read_input(fname):
    with Path(fname).open() as f:
        algorithm = {i for i,c in enumerate(next(f)) if c == "#"}
        next(f)
        pts = {(x, y) for y, line in enumerate(f) for x, c in enumerate(line) if c == "#"}
    return algorithm, Image(pts, True)

def enhancen(fname, n):
    algorithm, image = read_input(fname)
    for _ in range(n):
        image = image.enhance(algorithm)
    return image.census()

def part1(fname):
    return enhancen(fname, 2)

def test_part1():
    assert part1("day20_sample.txt") == 35

if __name__ == "__main__":
    print(f"part 1: {part1('day20_input.txt')}")

def part2(fname):
    return enhancen(fname, 50)

def test_part2():
    assert part2("day20_sample.txt") == 3351

if __name__ == "__main__":
    print(f"part 2: {part2('day20_input.txt')}")
