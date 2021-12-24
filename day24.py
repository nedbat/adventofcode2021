# https://adventofcode.com/2021/day/24

from pathlib import Path

def make_ast(fname):
    num_inputs = 0
    regs = dict.fromkeys("xyzw", ("num", 0))

    def valnode(val):
        try:
            val = int(val)
            return ("num", val)
        except ValueError:
            return regs[val]

    for line in Path(fname).open():
        match line.split():
            case ["inp", reg]:
                regs[reg] = ("inp", num_inputs)
                num_inputs += 1

            case ["add", reg, val]:
                r = regs[reg]
                if r == ("num", 0):
                    regs[reg] = valnode(val)
                elif val != ("num", 0):
                    regs[reg] = ("add", r, valnode(val))

            case ["mul", reg, "0"]:
                regs[reg] = ("num", 0)

            case ["mul", reg, val]:
                assert val != "1"
                regs[reg] = ("mul", regs[reg], valnode(val))

            case ["div", reg, "1"]:
                pass

            case ["div", reg, val]:
                r = regs[reg]
                if r != ("num", 0):
                    regs[reg] = ("div", r, valnode(val))

            case ["mod", reg, val]:
                assert val != "1"
                r = regs[reg]
                if r != ("num", 0):
                    regs[reg] = ("mod", r, valnode(val))

            case ["eql", reg, val]:
                r = regs[reg]
                if val == "0" and r[0] == "eql":
                    regs[reg] = ("neq", r[1], r[2])
                else:
                    regs[reg] = ("eql", r, valnode(val))

    return regs

def depth(node):
    if len(node) == 2:
        return 1
    else:
        return max(depth(node[1]), depth(node[2])) + 1

def lines(node):
    if len(node) == 2:
        return 1
    else:
        return 1 + lines(node[1]) + lines(node[2])

# regs = make_ast("day24_input.txt")
# for reg, ast in regs.items():
#     print(reg, depth(ast), lines(ast))

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
            [c[i].split()[2] for c in chunks])
