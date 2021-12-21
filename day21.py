# https://adventofcode.com/2021/day/21
# Dirac Dice

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
