# https://adventofcode.com/2021/day/1

with open("day01_input.txt") as f:
    depths = list(map(int, f))

increases = sum(b > a for a, b in zip(depths, depths[1:]))
print(f"Part 1: there are {increases} increases")
