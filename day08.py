# https://adventofcode.com/2021/day/8

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
