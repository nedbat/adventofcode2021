# https://adventofcode.com/2021/day/12

import collections
from pathlib import Path

import pytest


SAMPLE1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

SAMPLE2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

SAMPLE3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

def read_caves(text):
    caves = collections.defaultdict(list)
    for line in text.splitlines():
        a, b = line.split("-")
        caves[a].append(b)
        caves[b].append(a)
    return caves

def paths(caves):
    yield from paths_recursive(caves, "start", ["start"], {"start"})

def paths_recursive(caves, current, path, littles):
    for cave in caves[current]:
        if cave in littles:
            continue
        path.append(cave)
        if cave == "end":
            yield list(path)
        else:
            if cave.islower():
                littles.add(cave)
            yield from paths_recursive(caves, cave, path, littles)
            if cave.islower():
                littles.remove(cave)
        path.pop()

def test_paths():
    all_paths = set(",".join(p) for p in paths(read_caves(SAMPLE1)))
    assert all_paths == {
        "start,A,b,A,c,A,end",
        "start,A,b,A,end",
        "start,A,b,end",
        "start,A,c,A,b,A,end",
        "start,A,c,A,b,end",
        "start,A,c,A,end",
        "start,A,end",
        "start,b,A,c,A,end",
        "start,b,A,end",
        "start,b,end",
    }

@pytest.mark.parametrize("caves, paths_len", [(SAMPLE1, 10), (SAMPLE2, 19), (SAMPLE3, 226)])
def test_paths_len(caves, paths_len):
    assert len(list(paths(read_caves(caves)))) == paths_len

if __name__ == "__main__":
    all_paths = list(paths(read_caves(Path("day12_input.txt").read_text())))
    print(f"part 1: {len(all_paths)} paths")
