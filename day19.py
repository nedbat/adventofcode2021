# https://adventofcode.com/2021/day/19

import collections
import dataclasses
import itertools

from pathlib import Path
import numpy as np

np.set_printoptions(edgeitems=30, linewidth=100000, formatter={'float': (lambda f: format(f, '.1f'))})

# https://en.wikipedia.org/wiki/Matrix_multiplication#General_properties
# (A @ B).T == (B.T @ A.T)
# (A @ B) @ C == A @ (B @ C)
#
# Sets of points are like this:
# [ [ x1, y1, z1, 1],
#   [ x2, y2, z2, 1],
#   ...
# ]
#
# Transformation matrix:
#
# [[-1 0  0  0]
#  [0  1  0  0]
#  [0  0 -1  0]
#  [6  4 -4  1]]
# (this is transposed from usual notation like
# https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html)
#
# Transforming points:  pts @ M

@dataclasses.dataclass(frozen=True)
class Xyz:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def __sub__(self, other):
        return Xyz(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    @property
    def xyz(self):
        return self.x, self.y, self.z

    @property
    def xyz1(self):
        return self.x, self.y, self.z, 1

def points_from_array(a):
    """Make a set of Xyz() points from a row-wise numpy array of points."""
    return (Xyz(*map(round, r[:3])) for r in a)

def pairs(L):
    """All pairs in L, without both (a,b) and (b,a)."""
    return itertools.combinations(L, r=2)

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

    def calc_deltas(self):
        # For each pair of beacons, calculate an orientation-independent summary of their delta.
        self.deltas = set()
        self.delta_beacons = {}
        for b1, b2 in pairs(self.beacons):
            d = tuple(sorted(map(abs, (b1 - b2).xyz)))
            self.deltas.add(d)
            self.delta_beacons[d] = (b1, b2)

    def calc_beacon_deltas(self):
        # Make a map from beacon to the deltas it has with others
        self.beacon_deltas = collections.defaultdict(set)
        for d, (b1, b2) in self.delta_beacons.items():
            self.beacon_deltas[b1].add(d)
            self.beacon_deltas[b2].add(d)

    def beacon_array(self):
        return np.array([[*b.xyz, 1] for b in self.beacons])

    def overlap12_transform(self, other):
        """If these two have 12 beacons in common, return a transform from other to self."""
        s1, s2 = self, other
        d12 = s1.deltas & s2.deltas
        if len(d12) < 66:
            return None

        found = set()
        ptsa = []
        ptsb = []
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
            if b1a not in found:
                ptsa.append(b1a)
                ptsb.append(b2a)
                found.add(b1a)
            if b1b not in found:
                ptsa.append(b1b)
                ptsb.append(b2b)
                found.add(b1b)
            if len(ptsa) >= 4:
                break

        aa = np.array([p.xyz1 for p in ptsa[:4]])
        ab = np.array([p.xyz1 for p in ptsb[:4]])
        M = np.array([np.linalg.solve(ab, fv) for fv in aa.T]).T
        return M

def transforms_to_s0(scanners):
    """Compute the transform matrices from each scanner to the first."""
    nscanners = len(scanners)

    # Find the transforms from each scanner to scanners[0]
    xforms = [None] * nscanners
    tried = [False] * nscanners
    xforms[0] = np.identity(4)

    while any(xf is None for xf in xforms):
        for idst in range(nscanners):
            got_some = False
            if xforms[idst] is not None and not tried[idst]:
                for isrc in range(nscanners):
                    if xforms[isrc] is not None:
                        continue
                    xform = scanners[idst].overlap12_transform(scanners[isrc])
                    if xform is not None:
                        xforms[isrc] = xform @ xforms[idst]
                        got_some = True
            if got_some:
                tried[idst] = True
    return xforms

def part1(fname):
    scanners = read_scanners(fname)
    xforms = transforms_to_s0(scanners)

    # Transform all the beacons
    beacon_points = set()
    for scanner, xform in zip(scanners, xforms):
        beacon_points.update(points_from_array(scanner.beacon_array() @ xform))

    return len(beacon_points)

def test_part1():
    assert part1("day19_sample.txt") == 79

if __name__ == "__main__":
    print(f"part 1: {part1('day19_input.txt')}")

def scanner_locations(fname):
    scanners = read_scanners(fname)
    xforms = transforms_to_s0(scanners)
    locs = [next(points_from_array(np.array([[0,0,0,1]]) @ xf)) for xf in xforms]
    return locs

def test_scanner_locations():
    locs = scanner_locations("day19_sample.txt")
    assert locs[2] == Xyz(1105,-1205,1229)
    assert locs[3] == Xyz(-92,-2380,-20)

def part2(fname):
    locs = scanner_locations(fname)
    return max(sum(map(abs, (soa - sob).xyz)) for soa, sob in pairs(locs))

def test_part2():
    assert part2("day19_sample.txt") == 3621

if __name__ == "__main__":
    print(f"part 2: {part2('day19_input.txt')}")
