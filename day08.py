# https://adventofcode.com/2021/day/8

import itertools

def read_signals(fname: str) -> list[tuple[list[str], list[str]]]:
    signals = []
    with open(fname) as f:
        for line in f:
            a, b = line.split(" | ")
            signals.append((a.split(), b.split()))
    return signals

def part1(fname):
    signals = read_signals(fname)
    total = 0
    for _, output in signals:
        total += sum(1 for o in output if len(o) in {2, 3, 4, 7})
    return total

def test_part1():
    assert part1("day08_sample.txt") == 26

if __name__ == "__main__":
    ans = part1("day08_input.txt")
    print(f"part 1: {ans}")

# Part 2: try brute-forcing it...

DIGITS = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]

SEGS_TO_DIGIT = {seg: str(i) for i, seg in enumerate(DIGITS)}
VALID_DIGITS = set(DIGITS)

def all_mappings():
    for order in itertools.permutations("abcdefg"):
        yield dict(zip("abcdefg", order))

# Check that I understand the input file:
# signals = read_signals("day08_input.txt")
# for ins, outs in signals:
#     assert len(ins) == 10
#     assert {len(s) for s in ins} == {6,2,5,6,4,5,6,3,7,6}

def map_segments(segs: str, mapping: dict[str, str]) -> str:
    return "".join(sorted(mapping[s] for s in segs))

def is_valid_mapping(segss: list[str], mapping: dict[str, str]) -> bool:
    return all(map_segments(segs, mapping) in VALID_DIGITS for segs in segss)

def translate_output(outs: str, mapping: dict[str, str]) -> int:
    digits = []
    for out in outs:
        digits.append(SEGS_TO_DIGIT[map_segments(out, mapping)])
    return int("".join(digits))

def one_line_value(segs, outs):
    # find the right mapping.
    for m in all_mappings():
        if is_valid_mapping(segs, m):
            break
    # use the mapping to translate the outputs.
    return translate_output(outs, m)

def test_one_line_value():
    assert one_line_value(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(),
        "cdfeb fcadb cdfeb cdbaf".split(),
        ) == 5353

def part2(fname):
    signals = read_signals(fname)
    total = 0
    for segs, outs in signals:
        total += one_line_value(segs, outs)
    return total

def test_part2():
    assert part2("day08_sample.txt") == 61229

if __name__ == "__main__":
    ans = part2("day08_input.txt")
    print(f"part 2: {ans}")
