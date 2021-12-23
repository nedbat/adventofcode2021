# https://adventofcode.com/2021/day/23
# Amphipod

#############
#...........#
###B#A#A#D###
  #D#C#B#C#
  #########

# State:
# ("DB", "CA", "BA", "CD", "...........")
#                           xx.x.x.x.xx

SAMPLE = ["AB", "DC", "CB", "AD"]
INPUT = ["DB", "CA", "BA", "CD"]

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

    def __init__(self, roomtops, roombots, hallway):
        # room{tops,bots} are [None, 0, None, 1]
        self.roomtops = roomtops
        self.roombots = roombots
        # hallway is [None, None, None, 0, None, 1, ...]
        self.hallway = hallway

    @classmethod
    def first(cls, rooms):
        roomtops = ["ABCD".find(r[1]) for r in rooms]
        roombots = ["ABCD".find(r[0]) for r in rooms]
        return cls(roomtops, roombots, [None] * 11)

    def __hash__(self):
        return hash(tuple(self.roomtops)) + hash(tuple(self.roombots)) + hash(tuple(self.hallway))

    def __eq__(self, other):
        return self.roomtops == other.roomtops and self.roombots == other.roombots and self.hallway == other.hallway

    def is_goal(self):
        return self.roomtops == self.roombots == [0, 1, 2, 3]

    CHARS = dict(enumerate("ABCD")) | {None: "."}

    def print(self):
        print("#" + "".join(self.CHARS[v] for v in self.hallway) + "#")
        print("###" + "#".join(self.CHARS[v] for v in self.roomtops) + "###")
        print("  #" + "#".join(self.CHARS[v] for v in self.roombots) + "#  ")

    def next_states_print(self, cost):
        print("-" * 80)
        self.print()
        print()
        for ns in self._next_states(cost):
            print(f"cost: {ns[1]}")
            ns[0].print()
            yield ns
        import time; time.sleep(1)

    def next_states(self, cost):
        # Can anyone move out of a room?
        for roompos, amph in enumerate(self.roomtops):
            if amph is not None:
                hallroompos = self.HALLROOMPOS[roompos]
                for hallpos in self.HALLPOS:
                    if all(self.hallway[hp] is None for hp in from_to(hallroompos, hallpos)):
                        move_cost = (1 + abs(hallroompos - hallpos)) * 10 ** amph
                        new_hallway = self.hallway.copy()
                        new_hallway[hallpos] = amph
                        new_roomtops = self.roomtops.copy()
                        new_roomtops[roompos] = None
                        yield (AmphipodState(new_roomtops, self.roombots, new_hallway), cost + move_cost)
        for roompos, amph in enumerate(self.roombots):
            if self.roomtops[roompos] is None and amph is not None:
                hallroompos = self.HALLROOMPOS[roompos]
                for hallpos in self.HALLPOS:
                    if all(self.hallway[hp] is None for hp in from_to(hallroompos, hallpos)):
                        move_cost = (2 + abs(hallroompos - hallpos)) * 10 ** amph
                        new_hallway = self.hallway.copy()
                        new_hallway[hallpos] = amph
                        new_roombots = self.roombots.copy()
                        new_roombots[roompos] = None
                        yield (AmphipodState(self.roomtops, new_roombots, new_hallway), cost + move_cost)

        # Can anyone move from the hall into a room?
        for hallpos, amph in enumerate(self.hallway):
            if amph is None:
                continue
            roompos = self.HALLROOMPOS[amph]
            step_dir = cmp(roompos, hallpos)
            hallway_clear = all(self.hallway[hp] is None for hp in from_to(hallpos + step_dir, roompos))
            room_ok = self.roombots[amph] in (None, amph) and self.roomtops[amph] is None
            # print(f"@@ {hallpos=}, {amph=}, {hallway_clear=}, {roompos=}, {step_dir=}, {room_ok=}")
            if hallway_clear and room_ok:
                if self.roombots[amph] is None:
                    move_cost = (2 + abs(roompos - hallpos)) * 10 ** amph
                    new_hallway = self.hallway.copy()
                    new_hallway[hallpos] = None
                    new_roombots = self.roombots.copy()
                    new_roombots[amph] = amph
                    # print("@@@@")
                    yield (AmphipodState(self.roomtops, new_roombots, new_hallway), cost + move_cost)
                else:
                    move_cost = (1 + abs(roompos - hallpos)) * 10 ** amph
                    new_hallway = self.hallway.copy()
                    new_hallway[hallpos] = None
                    new_roomtops = self.roomtops.copy()
                    new_roomtops[amph] = amph
                    # print("@@@@")
                    yield (AmphipodState(new_roomtops, self.roombots, new_hallway), cost + move_cost)

    def guess_completion_cost(self):
        cost = 0
        for i, amph in enumerate(self.roomtops):
            if amph != i:
                cost += 10 ** i
        for i, amph in enumerate(self.roombots):
            if amph != i:
                cost += 2 * 10 ** i
        return cost

def part1(start):
    return astar.search(AmphipodState.first(start))

def test_part1():
    assert part1(SAMPLE) == 12521

if __name__ == "__main__":
    print(f"part 1: {part1(INPUT)}")
