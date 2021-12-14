# https://adventofcode.com/2021/day/14

import collections
import itertools
import re
from pathlib import Path

def read_input(fname):
    with Path(fname).open() as f:
        template = next(f).rstrip()
        next(f) # blank
        rules = []
        for line in f:
            rules.append(re.match(r"(..) -> (.)", line).groups())
    return template, dict(rules)

def step(polymer, rules):
    new = []
    for a, b in itertools.pairwise(polymer):
        pair = a + b
        new.append(a)
        new.append(rules[pair])
    new.append(b)
    return "".join(new)

def part1(fname):
    polymer, rules = read_input(fname)
    for _ in range(10):
        polymer = step(polymer, rules)
    count = collections.Counter(polymer)
    census = count.most_common()
    return census[0][1] - census[-1][1]

def test_part1():
    assert part1("day14_sample.txt") == 1588

if __name__ == "__main__":
    ans = part1("day14_input.txt")
    print(f"part 1: {ans}")
