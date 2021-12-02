# https://adventofcode.com/2021/day/2

def navigate(lines):
    hor = dep = 0
    for line in lines:
        match line.split():
            case ["forward", num]:
                hor += int(num)
            case ["down", num]:
                dep += int(num)
            case ["up", num]:
                dep -= int(num)
    return hor, dep

TEST = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".splitlines()

def test_navigate():
    assert navigate(TEST) == (15, 10)

if __name__ == "__main__":
    with open("day02_input.txt") as f:
        hor, dep = navigate(f)
    print(f"part 1: {hor * dep}")

def parse_line(line):
    word, num = line.split()
    return word, int(num)

def navigate2(lines):
    hor = dep = aim = 0
    for line in lines:
        match parse_line(line):
            case ["forward", num]:
                hor += num
                dep += aim * num
            case ["down", num]:
                aim += num
            case ["up", num]:
                aim -= num
    return hor, dep

def test_navigate2():
    assert navigate2(TEST) == (15, 60)

if __name__ == "__main__":
    with open("day02_input.txt") as f:
        hor, dep = navigate2(f)
    print(f"part 2: {hor * dep}")
