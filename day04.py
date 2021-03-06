# https://adventofcode.com/2021/day/4

from rich.console import Console

print = Console(highlight=False).print


class Board:
    def __init__(self, nums):
        self.nums = nums
        self.marked = set()
        self.positions = {n:(x,y) for y,ns in enumerate(nums) for x,n in enumerate(ns)}

    def __repr__(self):
        return f"<Board {self.nums=}>"

    def print(self):
        for row in self.nums:
            for num in row:
                marked = self.positions[num] in self.marked
                open = "[bold]" if marked else ""
                close = "[/bold]" if marked else ""
                print(f"{open}{num:3}{close}", end="")
            print()
        print()

    @classmethod
    def from_lines(cls, lines):
        nums = []
        for nline in range(5):
            line = next(lines)
            nums.append(list(map(int, line.split())))
        return cls(nums)

    def __contains__(self, num):
        return num in self.positions

    def mark_num(self, num):
        assert num in self
        self.marked.add(self.positions[num])

    def wins(self):
        """Is this a winning board?"""
        for i in range(5):
            if all((i, j) in self.marked for j in range(5)):
                return True
            if all((j, i) in self.marked for j in range(5)):
                return True
        return False

    def unmarked(self):
        return (n for n,pos in self.positions.items() if pos not in self.marked)

def read_input(fname):
    with open(fname) as f:
        nums = list(map(int, next(f).split(",")))
        boards = []
        while True:
            try:
                assert next(f).strip() == ""
            except:
                break
            boards.append(Board.from_lines(f))
    return nums, boards

def wins_first(fname):
    nums, boards = read_input(fname)
    for n in nums:
        for board in boards:
            if n in board:
                board.mark_num(n)
                if board.wins():
                    return sum(board.unmarked()) * n

def test_wins_first():
    assert wins_first("day04_sample.txt") == 4512

if __name__ == "__main__":
    ans = wins_first("day04_input.txt")
    print(f"part 1: {ans}")

def wins_last(fname):
    nums, boards = read_input(fname)
    boards = set(boards)
    for n in nums:
        winners = set()
        for board in boards:
            if n in board:
                board.mark_num(n)
                if board.wins():
                    if len(boards) == 1:
                        return sum(board.unmarked()) * n
                    else:
                        winners.add(board)

        boards -= winners

def test_wins_last():
    assert wins_last("day04_sample.txt") == 1924

if __name__ == "__main__":
    ans = wins_last("day04_input.txt")
    print(f"part 2: {ans}")
