# https://adventofcode.com/2021/day/3

import collections

TEST = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

def gamma_epsilon(text):
    lines = text.splitlines()
    columns = zip(*lines)
    counted = map(collections.Counter, columns)
    commonest = [c.most_common(1)[0][0] for c in counted]
    gamma = int("".join(commonest), 2)
    epsilon = (2 ** len(commonest) - 1) - gamma  
    return gamma, epsilon

def test_gamma_epsilon():
    assert gamma_epsilon(TEST) == (22, 9)

if __name__ == "__main__":
    with open("day03_input.txt") as f:
        gam, eps = gamma_epsilon(f.read())
    print(f"part 1: {gam * eps}")
