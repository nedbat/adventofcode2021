# https://adventofcode.com/2021/day/21
# Dirac Dice

import collections
import functools
import itertools

class DeterministicDie:
    def __init__(self):
        self.nums = itertools.cycle(range(1, 101))
        self.rolls = 0

    def __iter__(self):
        while True:
            self.rolls += 1
            yield next(self.nums)


SAMPLE = [4, 8]
INPUT = [4, 2]

class Player:
    def __init__(self, start):
        self.pos = start - 1
        self.score = 0

    def move(self, die):
        rolls = next(die) + next(die) + next(die)
        self.pos = (self.pos + rolls) % 10
        self.score += self.pos + 1

def game(p1, p2, die, goal):
    diter = iter(die)
    while True:
        p1.move(diter)
        #print(f"p1: {p1.pos=}, {p1.score=}")
        if p1.score >= goal:
            loser = p2
            break
        p2.move(diter)
        #print(f"p2: {p2.pos=}, {p2.score=}")
        if p2.score >= goal:
            loser = p1
            break
    return die.rolls * loser.score

def part1(s1, s2):
    return game(Player(s1), Player(s2), DeterministicDie(), 1000)

def test_part1():
    assert part1(*SAMPLE) == 739785

if __name__ == "__main__":
    print(f"part 1: {part1(*INPUT)}")


SPLITS = list(collections.Counter(sum(d) for d in itertools.product([1,2,3], repeat=3)).items())

@functools.cache
def num_wins(p1, s1, p2, s2, goal):
    """
    Player 1 is at p1 with a score of s1.
    Player 2 is at p2 with a score of s2.
    Return a pair, the number of universes each wins in.
    """
    if s1 >= goal:
        return 1, 0
    if s2 >= goal:
        return 0, 1
    tw1 = tw2 = 0
    for rolls, num in SPLITS:
        np1 = (p1 + rolls) % 10
        ns1 = s1 + np1 + 1
        w2, w1 = num_wins(p2, s2, np1, ns1, goal)
        tw1 += w1 * num
        tw2 += w2 * num
    return tw1, tw2

def part2(p1, p2):
    w1, w2 = num_wins(p1-1, 0, p2-1, 0, 21)
    return max(w1, w2)

def test_part2():
    assert part2(*SAMPLE) == 444356092776315

if __name__ == "__main__":
    print(f"part 2: {part2(*INPUT)}")
