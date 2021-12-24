# https://adventofcode.com/2021/day/24

from pathlib import Path

if 0:
    lines = [l.strip() for l in Path("day24_input.txt").open()]
    chunks = [lines[i:i+18] for i in range(0, len(lines), 18)]
    for i in range(18):
        if len(set(c[i] for c in chunks)) == 1:
            print(chunks[0][i])
        else:
            assert len(set(c[i].split()[0] for c in chunks)) == 1
            assert len(set(c[i].split()[1] for c in chunks)) == 1
            print(
                chunks[0][i].split()[0],
                chunks[0][i].split()[1],
                [int(c[i].split()[2]) for c in chunks])

# inp w
# mul x 0
# add x z
# mod x 26
# div z [1, 1, 1, 26, 26, 1, 1, 26, 1, 26, 1, 26, 26, 26]
# add x [12, 12, 12, -9, -9, 14, 14, -10, 15, -2, 11, -15, -9, -3]
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y [9, 4, 2, 5, 1, 6, 11, 15, 7, 12, 15, 9, 12, 12]
# mul y x
# add z y

# Hand translated:

if 0:
    for divz, addx, addy in zip(divzs, addxs, addys):
        w = inp()
        x = z % 26
        z //= divz
        x += addx
        x = (x != w)
        y = 25 * x + 1
        z *= y
        y = (w + addy) * x
        z += y

def z26(z):
    digits = []
    for _ in range(14):
        digits.append(z % 26)
        z //= 26
    return digits[::-1]

divzs = [ 1,  1,  1, 26, 26,  1,  1,  26,  1, 26,  1,  26, 26, 26]
addxs = [12, 12, 12, -9, -9, 14, 14, -10, 15, -2, 11, -15, -9, -3]
addys = [ 9,  4,  2,  5,  1,  6, 11,  15,  7, 12, 15,   9, 12, 12]
inps =  [ 3,  9,  9,  2,  4,  9,  8,   9,  4,  9,  9,   9,  6,  9]

z = 0
for inp, divz, addx, addy in zip(inps, divzs, addxs, addys):
    print(inp, z26(z))
    x = (z % 26) + addx
    z //= divz
    #print(f"{inp=}, {x=}")
    if inp != x:
        z *= 26
        z += inp + addy
print(z26(z))

# 39924989499969
