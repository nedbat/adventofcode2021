# https://adventofcode.com/2021/day/22
# Reactor Reboot

import dataclasses
import itertools
import re
from pathlib import Path

import pytest

@dataclasses.dataclass(frozen=True)
class Xyz:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def __add__(self, other):
        return Xyz(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        return Xyz(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )


def read_steps(fname):
    for line in Path(fname).open():
        op, _, xyz_text = line.partition(" ")
        xyz = list(map(int, re.findall(r"-?\d+", xyz_text)))
        xyzl = Xyz(*xyz[::2])
        xyzh = Xyz(*xyz[1::2]) + Xyz(1, 1, 1)
        assert xyzl.x < xyzh.x and xyzl.y < xyzh.y and xyzl.z < xyzh.z
        yield [op, xyzl, xyzh]

def clip_range(lo, hi, minlo, maxhi):
    return range(max(lo, minlo), min(hi, maxhi))

@pytest.mark.parametrize("lo, hi, nums", [
    (-1, 3, [-1, 0, 1, 2]),
    (-5, 3, [-3, -2, -1, 0, 1, 2]),
    (1, 6, [1, 2, 3]),
    (-10, -5, []),
])
def test_clip_range(lo, hi, nums):
    assert list(clip_range(lo, hi, -3, 4)) == nums

def count_cubes(steps, ol, oh):
    cubes = set()
    for op, xyzl, xyzh in steps:
        xr = clip_range(xyzl.x, xyzh.x, ol.x, oh.x)
        yr = clip_range(xyzl.y, xyzh.y, ol.y, oh.y)
        zr = clip_range(xyzl.z, xyzh.z, ol.z, oh.z)
        for xyz in itertools.product(xr, yr, zr):
            if op == "on":
                cubes.add(xyz)
            elif xyz in cubes:
                cubes.remove(xyz)
    return len(cubes)

def part1(fname):
    ol = Xyz(-50, -50, -50)
    oh = Xyz(51, 51, 51)
    return count_cubes(read_steps(fname), ol, oh)

def test_part1():
    assert part1("day22_sample.txt") == 590784

if __name__ == "__main__":
    print(f"part 1: {part1('day22_input.txt')}")

# Too many to count individually, so use an octtree representation:
#
#   True or False means the octbox is entirely on or off
#
#   [midpoint, clll, cllh, clhl, clhh, chll, chlh, chhl, chhh] means the cube
#   is subdivided into 8 octboxes.
#
# Strict binary takes too long, use adaptive subsivision.

def run_step(oct, ol, oh, op, xyzl, xyzh):

    # Are we already in a filled region, and this op is a no-op?
    if oct is True and op == "on":
        return True
    if oct is False and op == "off":
        return False

    # Are we in a zero-volumn octbox?
    sides = oh - ol
    if sides.x * sides.y * sides.z == 0:
        return False

    # Is the desired cube entirely outside this octbox?
    if (
        oh.x <= xyzl.x or xyzh.x <= ol.x or
        oh.y <= xyzl.y or xyzh.y <= ol.y or
        oh.z <= xyzl.z or xyzh.z <= ol.z
    ):
        return oct

    # Is this octbox entirely within the desired cube?
    if (
        xyzl.x <= ol.x and oh.x <= xyzh.x and
        xyzl.y <= ol.y and oh.y <= xyzh.y and
        xyzl.z <= ol.z and oh.z <= xyzh.z
    ):
        return op == "on"

    # Recurse into the octtree.
    if isinstance(oct, bool):
        # Have to subdivide. use the lll or hhh point of the region or octbox to split.
        omid = Xyz(max(ol.x, xyzl.x), max(ol.y, xyzl.y), max(ol.z, xyzl.z))
        if omid == ol:
            omid = Xyz(min(oh.x, xyzh.x), min(oh.y, xyzh.y), min(oh.z, xyzh.z))
            assert omid != oh
        oct = [omid] + [oct] * 8

    omid = oct[0]
    return [
        omid,
        run_step(oct[1], Xyz(ol.x, ol.y, ol.z), Xyz(omid.x, omid.y, omid.z), op, xyzl, xyzh),
        run_step(oct[2], Xyz(ol.x, ol.y, omid.z), Xyz(omid.x, omid.y, oh.z), op, xyzl, xyzh),
        run_step(oct[3], Xyz(ol.x, omid.y, ol.z), Xyz(omid.x, oh.y, omid.z), op, xyzl, xyzh),
        run_step(oct[4], Xyz(ol.x, omid.y, omid.z), Xyz(omid.x, oh.y, oh.z), op, xyzl, xyzh),
        run_step(oct[5], Xyz(omid.x, ol.y, ol.z), Xyz(oh.x, omid.y, omid.z), op, xyzl, xyzh),
        run_step(oct[6], Xyz(omid.x, ol.y, omid.z), Xyz(oh.x, omid.y, oh.z), op, xyzl, xyzh),
        run_step(oct[7], Xyz(omid.x, omid.y, ol.z), Xyz(oh.x, oh.y, omid.z), op, xyzl, xyzh),
        run_step(oct[8], Xyz(omid.x, omid.y, omid.z), Xyz(oh.x, oh.y, oh.z), op, xyzl, xyzh),
    ]


def count_octtree_cubes(oct, ol, oh):
    sides = oh - ol
    if oct is False:
        return 0
    if oct is True:
        return sides.x * sides.y * sides.z

    omid = oct[0]
    return sum([
        count_octtree_cubes(oct[1], Xyz(ol.x, ol.y, ol.z), Xyz(omid.x, omid.y, omid.z)),
        count_octtree_cubes(oct[2], Xyz(ol.x, ol.y, omid.z), Xyz(omid.x, omid.y, oh.z)),
        count_octtree_cubes(oct[3], Xyz(ol.x, omid.y, ol.z), Xyz(omid.x, oh.y, omid.z)),
        count_octtree_cubes(oct[4], Xyz(ol.x, omid.y, omid.z), Xyz(omid.x, oh.y, oh.z)),
        count_octtree_cubes(oct[5], Xyz(omid.x, ol.y, ol.z), Xyz(oh.x, omid.y, omid.z)),
        count_octtree_cubes(oct[6], Xyz(omid.x, ol.y, omid.z), Xyz(oh.x, omid.y, oh.z)),
        count_octtree_cubes(oct[7], Xyz(omid.x, omid.y, ol.z), Xyz(oh.x, oh.y, omid.z)),
        count_octtree_cubes(oct[8], Xyz(omid.x, omid.y, omid.z), Xyz(oh.x, oh.y, oh.z)),
    ])

def part2(fname):
    oct = False
    l = -(2 ** 17)
    h = l + 2 ** 18
    ol = Xyz(l, l, l)
    oh = Xyz(h, h, h)
    for op, xyzl, xyzh in read_steps(fname):
        oct = run_step(oct, ol, oh, op, xyzl, xyzh)
    return count_octtree_cubes(oct, ol, oh)

def test_part2():
    assert part2("day22_sample2.txt") == 2758514936282235

if __name__ == "__main__":
    print(f"part 2: {part2('day22_input.txt')}")
