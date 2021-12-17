# https://adventofcode.com/2021/day/17

import dataclasses
import itertools
from typing import Iterable, Tuple

import pytest

@dataclasses.dataclass
class Pt:
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

def positions(vel: Pt) -> Iterable[Tuple[Pt, Pt]]:
    """Produce a stream of (position, velocity) points."""
    assert vel.x > 0
    xy = Pt(0, 0)
    while True:
        yield xy, vel
        xy += vel
        if vel.x > 0:
            vel += Pt(-1, -1)
        else:
            vel += Pt(0, -1)


def test_positions():
    assert [pt for pt, vel in itertools.islice(positions(Pt(7, 2)), 8)] == [
        Pt(0, 0), Pt(7, 2), Pt(13, 3), Pt(18, 3), Pt(22, 2), Pt(25, 0), Pt(27, -3), Pt(28, -7)
    ]

INPUT = Pt(192, -89), Pt(251, -59)
SAMPLE = Pt(20, -10), Pt(30, -5)

def check_trajectory(vel, llr, urr):
    maxy = 0
    for pt, vel in positions(vel):
        #print(f"{pt=}, {vel=}")
        if pt.y > maxy:
            maxy = pt.y
        if (llr.x <= pt.x <= urr.x) and (llr.y <= pt.y <= urr.y):
            return True, maxy, "within"
        if vel.x == 0 and pt.x < llr.x:
            return False, maxy, "fell short"
        if vel.x == 0 and pt.x > urr.x:
            return False, maxy, "too wide"
        if pt.y < llr.y:
            return False, maxy, "below"
        if pt.x > urr.x:
            return False, maxy, "overshot"

@pytest.mark.parametrize("vel, res", [
    (Pt(7, 2), (True, 3, "within")),
    (Pt(6, 3), (True, 6, "within")),
    (Pt(9, 0), (True, 0, "within")),
    (Pt(17, -4), (False, 0, "overshot")),
    (Pt(6, 9), (True, 45, "within")),
])
def test_check_trajectory(vel, res):
    assert check_trajectory(vel, *SAMPLE) == res

def pt_range(lx, ux, ly, uy):
    for x in range(lx, ux + 1):
        for y in range(ly, uy + 1):
            yield Pt(x, y)

def brute(llr, urr):
    # Find the minx that will put the vertical fall into the range.
    minvx_limit = 0
    for minvx in itertools.count():
        minvx_limit += minvx
        if minvx_limit >= llr.x:
            break
    # maxx is the last column of the target. Beyond that, the first step
    # falls to the right of the range.
    maxvx = urr.x
    # miny is the lowest row of the target. Beyond that, the first step
    # falls below the range.
    minvy = llr.y 
    # maxy is the same as minvy, but upward. Once the y velocity changes to
    # zero and the projectile starts coming down, the same y velocities will
    # repeat on the way down in the reverse order. So the projectile will
    # eventually land on y=0 again. Then the next step down will be the same
    # as the initial velocity, but downward. So the fastest that can land in
    # the range is the lower row of the target.
    maxvy = -llr.y

    max_maxy = 0
    num_ok = 0
    for vel in pt_range(minvx, maxvx, minvy, maxvy):
        ok, maxy, why = check_trajectory(vel, llr, urr)
        if ok:
            num_ok += 1
            if maxy > max_maxy:
                max_maxy = maxy

    return max_maxy, num_ok

def test_brute():
    assert brute(*SAMPLE) == (45, 112)

if __name__ == "__main__":
    highest, num_ok = brute(*INPUT)
    print(f"part 1: {highest}")
    print(f"part 2: {num_ok}")
