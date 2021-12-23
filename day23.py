# https://adventofcode.com/2021/day/23
# Amphipod

#############
#...........#
###B#A#A#D###
  #D#C#B#C#
  #########

SAMPLE = ["BCBD", "ADCA"]
INPUT = ["BAAD", "DCBC"]

import astar

def from_to(a, b):
    if a > b:
        a, b = b, a
    return range(a, b + 1)

def cmp(a, b):
    return (a > b) - (a < b)

class AmphipodState(astar.State):
    HALLROOMPOS = [2, 4, 6, 8]
    HALLPOS = [0, 1, 3, 5, 7, 9, 10]

    def __init__(self, roomrows, hallway, prev=None, cost=0):
        # roomrows are [[None, 0, None, 1], ...]
        self.roomrows = roomrows
        # hallway is [None, None, None, 0, None, 1, ...]
        self.hallway = hallway
        self.prev = prev
        self.cost = cost

    @classmethod
    def first(cls, rooms, part2=False):
        rtop = ["ABCD".find(a) for a in rooms[0]]
        rbottom = ["ABCD".find(a) for a in rooms[1]]
        if part2:
            roomrows = [
                rtop,
                [3, 2, 1, 0],
                [3, 1, 0, 2],
                rbottom,
            ]
        else:
            roomrows = [rtop, rbottom]
        return cls(roomrows, [None] * 11)

    def __hash__(self):
        return sum(hash(tuple(r)) for r in self.roomrows) + hash(tuple(self.hallway))

    def __eq__(self, other):
        return self.roomrows == other.roomrows and self.hallway == other.hallway

    def is_goal(self):
        return all(r == [0, 1, 2, 3] for r in self.roomrows)

    CHARS = dict(enumerate("ABCD")) | {None: "."}

    def print(self):
        print(f"{self.cost}$:")
        print("#" + "".join(self.CHARS[v] for v in self.hallway) + "#")
        for i, r in enumerate(self.roomrows):
            end = "##" if i == 0 else "  "
            print(end + "#" + "#".join(self.CHARS[v] for v in r) + "#" + end)

    def print_path(self):
        states = []
        s = self
        while s is not None:
            states.append(s)
            s = s.prev
        for s in reversed(states):
            s.print()
            print()

    def next_states_print(self, cost):
        # For printing random sample of states, for debugging.
        import random
        nss = self.next_states_work(cost)
        if random.random() > .999:
            print("-" * 80)
            self.print()
            print()
            for ns in nss:
                ns[0].print()
                yield ns
            import time; time.sleep(1)
        else:
            yield from nss

    def next_states_work(self, cost):
        # Can anyone move out of a room?
        for irow, row in enumerate(self.roomrows):
            for roompos, amph in enumerate(row):
                if amph is None:
                    continue
                if any(self.roomrows[above][roompos] is not None for above in range(irow)):
                    # we're blocked from exiting this room
                    continue
                if amph == roompos and all(self.roomrows[below][roompos] == amph for below in range(irow+1, len(self.roomrows))):
                    # we're where we should be, don't move
                    continue
                hallroompos = self.HALLROOMPOS[roompos]
                for hallpos in self.HALLPOS:
                    if all(self.hallway[hp] is None for hp in from_to(hallroompos, hallpos)):
                        move_cost = (irow + 1 + abs(hallroompos - hallpos)) * 10 ** amph
                        new_hallway = self.hallway.copy()
                        new_hallway[hallpos] = amph
                        new_row = self.roomrows[irow].copy()
                        new_row[roompos] = None
                        new_roomrows = self.roomrows.copy()
                        new_roomrows[irow] = new_row
                        yield (AmphipodState(new_roomrows, new_hallway), cost + move_cost)

        # Can anyone move from the hall into a room?
        for hallpos, amph in enumerate(self.hallway):
            if amph is None:
                continue
            hallroompos = self.HALLROOMPOS[amph]
            step_dir = cmp(hallroompos, hallpos)
            hallway_clear = all(self.hallway[hp] is None for hp in from_to(hallpos + step_dir, hallroompos))
            if hallway_clear:
                for irow in range(len(self.roomrows) - 1, -1, -1):
                    row = self.roomrows[irow]
                    if row[amph] is None:
                        move_cost = (irow + 1 + abs(hallroompos - hallpos)) * 10 ** amph
                        new_hallway = self.hallway.copy()
                        new_hallway[hallpos] = None
                        new_row = self.roomrows[irow].copy()
                        new_row[amph] = amph
                        new_roomrows = self.roomrows.copy()
                        new_roomrows[irow] = new_row
                        yield (AmphipodState(new_roomrows, new_hallway), cost + move_cost)
                        break # No point moving to a higher row
                    elif row[amph] != amph:
                        # There's a wrong amph here, so don't move into this room
                        break

    next_states = next_states_work

    def guess_completion_cost(self):
        cost = 0
        for irow, row in enumerate(self.roomrows):
            for i, amph in enumerate(row):
                if amph != i:
                    cost += (irow + 1) * 10 ** i
        return cost

def part1(start):
    best, cost = astar.search(AmphipodState.first(start))
    #best.print_path()
    return cost

def test_part1():
    assert part1(SAMPLE) == 12521

if __name__ == "__main__":
    print(f"part 1: {part1(INPUT)}")

def part2(start):
    best, cost = astar.search(AmphipodState.first(start, part2=True))
    #best.print_path()
    return cost

def test_part2():
    assert part2(SAMPLE) == 44169

if __name__ == "__main__":
    print(f"part 2: {part2(INPUT)}")
