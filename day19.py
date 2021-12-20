# https://adventofcode.com/2021/day/19

import collections
import dataclasses

from pathlib import Path
import numpy as np

@dataclasses.dataclass(frozen=True)
class Xyz:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def __sub__(self, other):
        return (
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

def pairs(L):
    """All pairs in L, without both (a,b) and (b,a)."""
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            yield L[i], L[j]

def read_scanners(fname):
    beaconss = []
    with Path(fname).open() as f:
        for line in f:
            if line.startswith("---"):
                beaconss.append([])
            elif line.strip():
                xyz = Xyz(*map(int, line.split(",")))
                beaconss[-1].append(xyz)
    return list(map(Scanner, beaconss))

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.calc_deltas()
        self.calc_beacon_deltas()

    hasher = np.array([2000*2000, 2000, 1])

    def calc_deltas(self):
        # For each pair of beacons, calculate an orientation-independent summary of their delta.
        self.deltas = set()
        self.delta_beacons = {}
        for b1, b2 in pairs(self.beacons):
            d = tuple(sorted(map(abs, b1 - b2)))
            self.deltas.add(d)
            self.delta_beacons[d] = (b1, b2)

    def calc_beacon_deltas(self):
        # Make a map from beacon to the deltas it has with others
        self.beacon_deltas = collections.defaultdict(set)
        for d, (b1, b2) in self.delta_beacons.items():
            self.beacon_deltas[b1].add(d)
            self.beacon_deltas[b2].add(d)


def part1(fname):
    scanners = read_scanners(fname)
    equiv = {}

    def eq(x, y):
        if x in equiv:
            s = equiv[y] = equiv[x]
        elif y in equiv:
            s = equiv[x] = equiv[y]
        else:
            s = equiv[x] = equiv[y] = set()
        s.add(y)
        s.add(x)

    for s1, s2 in pairs(scanners):
        d12 = s1.deltas & s2.deltas
        if len(d12) >= 66:
            # There are 12 beacons in common
            for d in d12:
                b1a, b1b = s1.delta_beacons[d]
                b2a, b2b = s2.delta_beacons[d]
                b1ad = s1.beacon_deltas[b1a] & d12
                b1bd = s1.beacon_deltas[b1b] & d12
                b2ad = s2.beacon_deltas[b2a] & d12
                b2bd = s2.beacon_deltas[b2b] & d12
                if b1ad != b2ad:
                    b2a, b2b = b2b, b2a
                else:
                    assert b1ad == b2ad
                eq(b1a, b2a)
                eq(b1b, b2b)

    # Now add the beacons that were not in any 12-beacon overlap.
    for s in scanners:
        for b in s.beacons:
            if b not in equiv:
                equiv[b] = {b}

    equiv_ids = set(frozenset(s) for s in equiv.values())
    return len(equiv_ids)

def test_part1():
    assert part1("day19_sample.txt") == 79

if __name__ == "__main__":
    print(f"part 1: {part1('day19_input.txt')}")
