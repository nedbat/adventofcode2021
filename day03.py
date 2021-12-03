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

def commonest(nums: list[str], column: int, most: bool) -> str:
    counted = collections.Counter(n[column] for n in nums)
    hi, lo = counted.most_common()
    if hi[1] == lo[1]:
        return "1" if most else "0"
    elif most:
        return hi[0]
    else:
        return lo[0]

def bit_criteria(text: str, most: bool):
    nums = text.splitlines()
    for column in range(len(nums[0])):
        digit = commonest(nums, column, most)
        nums = [n for n in nums if n[column] == digit]
        if len(nums) == 1:
            return int(nums[0], 2)
    assert False

def oxy_co2(text):
    return (
        bit_criteria(text, most=True),
        bit_criteria(text, most=False),
    )

def test_oxy_co2():
    assert oxy_co2(TEST) == (23, 10)

if __name__ == "__main__":
    with open("day03_input.txt") as f:
        oxy, co2 = oxy_co2(f.read())
    print(f"part 2: {oxy * co2}")
