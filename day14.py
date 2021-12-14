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


# Part 1 literally made each polymer. Part 2 can't, they get too long.

def step2(polypairs, rules):
    new = collections.Counter()
    for pair, count in polypairs.items():
        a, b = pair
        middle = rules[pair]
        new[a + middle] += count
        new[middle + b] += count
    return new

def part2(fname):
    polymer, rules = read_input(fname)
    polypairs = collections.Counter()
    # turn the polymer into a count of pairs
    for a, b in itertools.pairwise(polymer):
        polypairs[a + b] += 1
    # run for 40 steps
    for _ in range(40):
        polypairs = step2(polypairs, rules)
    # count individual elements: this double counts, except
    # for the two elements at the ends.
    elements = collections.Counter()
    for (a, b), count in polypairs.items():
        elements[a] += count
        elements[b] += count
    # get the ends
    elements[polymer[0]] += 1
    elements[polymer[-1]] += 1
    census = elements.most_common()
    return (census[0][1] - census[-1][1]) // 2

def test_part2():
    assert part2("day14_sample.txt") == 2188189693529

if __name__ == "__main__":
    ans = part2("day14_input.txt")
    print(f"part 2: {ans}")

