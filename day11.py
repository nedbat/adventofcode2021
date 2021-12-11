# https://adventofcode.com/2021/day/11

import itertools
from pathlib import Path

import pytest
from rich.console import Console

def neighbors(x, y):
    if y > 0:
        if x > 0:
            yield (x - 1, y - 1)
        yield (x, y - 1)
        if x < 9:
            yield (x + 1, y - 1)
    if x > 0:
        yield (x - 1, y)
    if x < 9:
        yield (x + 1, y)
    if y < 9:
        if x > 0:
            yield (x - 1, y + 1)
        yield (x, y + 1)
        if x < 9:
            yield (x + 1, y + 1)

def rangexy(xstop, ystop):
    return itertools.product(range(xstop), range(ystop))

class Grid:
    def __init__(self, text):
        self.octopi = [[int(c) for c in l] for l in text.splitlines()]

    @classmethod
    def from_file(cls, fname):
        return cls(Path(fname).read_text())

    def print(self):
        con = Console(highlight=False)
        for l in self.octopi:
            for c in l:
                if c == 0:
                    con.print("[bold]0[/bold]", end="")
                else:
                    con.print(c, end="")
            print()

    def step(self):
        # first, increase the level by 1.
        for x, y in rangexy(10, 10):
            self.octopi[y][x] += 1
        # any octopus with an energy level greater than 9 flashes.
        flashes = {}
        for x, y in rangexy(10, 10):
            if self.octopi[y][x] > 9:
                flashes[(x, y)] = "will"
        while True:
            will_flash = [(x, y) for (x, y), s in flashes.items() if s == "will"]
            if not will_flash:
                break
            for x, y in will_flash:
                flashes[(x, y)] = "did"
                for nx, ny in neighbors(x, y):
                    if (nx, ny) in flashes:
                        continue
                    self.octopi[ny][nx] += 1
                    if self.octopi[ny][nx] > 9:
                        flashes[(nx, ny)] = "will"
        # any octopus that flashed has its energy level set to 0.
        for x, y in flashes:
            self.octopi[y][x] = 0
        
        return len(flashes)


def part1(fname, nsteps):
    grid = Grid.from_file(fname)
    #grid.print()
    #print()
    total = 0
    for _ in range(nsteps):
        flashes = grid.step()
        total += flashes
        # grid.print()
        # print(f"{flashes=}\n")
    #print(f"{total=}")
    return total

@pytest.mark.parametrize("nsteps, total", [(10, 204), (100, 1656)])
def test_part1(nsteps, total):
    assert part1("day11_sample.txt", nsteps) == total

if __name__ == "__main__":
    ans = part1("day11_input.txt", 100)
    print(f"part 1: {ans}")
