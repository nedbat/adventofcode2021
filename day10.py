# https://adventofcode.com/2021/day/10

from pathlib import Path

import pytest

PAIRS = "()[]{}<>"

OPENS = dict(zip(PAIRS[1::2], PAIRS[::2]))

def corrupted(s):
    """Returns the first wrong char, or None if not corrupted"""
    stack = []
    for c in s:
        if c in "([{<":
            stack.append(c)
        else:
            if stack[-1] == OPENS[c]:
                stack.pop()
            else:
                return c
    return None


VALIDS = [
    "([])", "{()()()}", "<([{}])>", "[<>({}){}[([])<>]]", "(((((((((())))))))))",
]

@pytest.mark.parametrize("s", VALIDS)
def test_corrupted_good(s):
    assert corrupted(s) is None

@pytest.mark.parametrize("s, c", [
    ("{([(<{}[<>[]}>{[]{[(<()>", "}"),  # Expected ], but found } instead.
    ("[[<[([]))<([[{}[[()]]]", ")"),    # Expected ], but found ) instead.
    ("[{[{({}]{}}([{[{{{}}([]", "]"),   # Expected ), but found ] instead.
    ("[<(<(<(<{}))><([]([]()", ")"),    # Expected >, but found ) instead.
    ("<{([([[(<>()){}]>(<<{{", ">"),    # Expected ], but found > instead.
])
def test_corrupted_bad(s, c):
    assert corrupted(s) == c

POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137, None: 0}

def part1(fname):
    score = 0
    for line in Path(fname).open():
        c = corrupted(line.strip())
        score += POINTS[c]
    return score

def test_part1():
    assert part1("day10_sample.txt") == 26397

if __name__ == "__main__":
    ans = part1("day10_input.txt")
    print(f"part 1: {ans}")
