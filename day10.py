# https://adventofcode.com/2021/day/10

import statistics
from pathlib import Path

import pytest

PAIRS = "()[]{}<>"

OPENS = dict(zip(PAIRS[1::2], PAIRS[::2]))
CLOSES = dict(zip(PAIRS[::2], PAIRS[1::2]))

def check_syntax(s):
    stack = []
    for c in s:
        if c in "([{<":
            stack.append(c)
        else:
            if stack[-1] == OPENS[c]:
                stack.pop()
            else:
                return c, stack
    return None, stack

def corrupted(s):
    """Returns the first wrong char, or None if not corrupted"""
    c, stack = check_syntax(s)
    return c


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

def completion(s):
    c, stack = check_syntax(s)
    if c is None and stack:
        return "".join(CLOSES[c] for c in stack[::-1])
    return None

@pytest.mark.parametrize("s, comp", [
    ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]"),
    ("[(()[<>])]({[<{<<[]>>(", ")}>]})"),
    ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))"),
    ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>"),
    ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>"),
])
def test_completion_needed(s, comp):
    assert completion(s) == comp

@pytest.mark.parametrize("s", VALIDS)
def test_completion_not_needed(s):
    assert completion(s) is None

def part2(fname):
    scores = []
    for line in Path(fname).open():
        comp = completion(line.strip())
        if comp:
            score = 0
            for c in comp:
                score *= 5
                score += " )]}>".find(c)
            scores.append(score)
    return statistics.median(scores)

def test_part2():
    assert part2("day10_sample.txt") == 288957

if __name__ == "__main__":
    ans = part2("day10_input.txt")
    print(f"part 2: {ans}")
