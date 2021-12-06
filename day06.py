# https://adventofcode.com/2021/day/6

import itertools

import pytest

TEST = [3,4,3,1,2]
INPUT = [1,1,1,1,1,5,1,1,1,5,1,1,3,1,5,1,4,1,5,1,2,5,1,1,1,1,3,1,4,5,1,1,2,1,1,1,2,4,3,2,1,1,2,1,5,4,4,1,4,1,1,1,4,1,3,1,1,1,2,1,1,1,1,1,1,1,5,4,4,2,4,5,2,1,5,3,1,3,3,1,1,5,4,1,1,3,5,1,1,1,4,4,2,4,1,1,4,1,1,2,1,1,1,2,1,5,2,5,1,1,1,4,1,2,1,1,1,2,2,1,3,1,4,4,1,1,3,1,4,1,1,1,2,5,5,1,4,1,4,4,1,4,1,2,4,1,1,4,1,3,4,4,1,1,5,3,1,1,5,1,3,4,2,1,3,1,3,1,1,1,1,1,1,1,1,1,4,5,1,1,1,1,3,1,1,5,1,1,4,1,1,3,1,1,5,2,1,4,4,1,4,1,2,1,1,1,1,2,1,4,1,1,2,5,1,4,4,1,1,1,4,1,1,1,5,3,1,4,1,4,1,1,3,5,3,5,5,5,1,5,1,1,1,1,1,1,1,1,2,3,3,3,3,4,2,1,1,4,5,3,1,1,5,5,1,1,2,1,4,1,3,5,1,1,1,5,2,2,1,4,2,1,1,4,1,3,1,1,1,3,1,5,1,5,1,1,4,1,2,1]

# Literal solution: actually track each fish:

def run(fish):
    while True:
        yield fish
        fish = [6 if f == 0 else (f - 1) for f in fish] + [8] * fish.count(0)

def after(fish, n):
    return len(next(itertools.islice(run(fish), n, n+1)))

@pytest.mark.parametrize("fish, ans", [
    (TEST, 5934),
    (INPUT, 374994),
])
def test_after(fish, ans):
    assert after(fish, 80) == ans

if __name__ == "__main__":
    print(f"part 1: {after(INPUT, 80)}")

# Literal solution will take too long, and we don't need to track each fish.
# Instead track how many of each age fish there are.

def run_smarter(fish):
    census = [fish.count(i) for i in range(7)] + [0, 0]
    while True:
        yield sum(census)
        nspawn = census[0]
        census = census[1:] + [nspawn]
        census[6] += nspawn

def after_smarter(fish, n):
    return next(itertools.islice(run_smarter(fish), n, n+1))

@pytest.mark.parametrize("fish, ans", [
    (TEST, 5934),
    (INPUT, 374994),
])
def test_after_smarter(fish, ans):
    assert after_smarter(fish, 80) == ans

if __name__ == "__main__":
    print(f"part 2: {after_smarter(INPUT, 256)}")
