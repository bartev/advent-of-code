#!/usr/bin/env python

"""
Create a Puzzle class
* labmap: a list of rows (strs)
* Guard's position is either [^, >, v, <]
* `#` is an obstacle
* `.` is a free space

* cur_pos: (row, col) of guard
* cur_dir: Direction guard is traveling

methods:
* find the guard
* get guard's position in a row
* travel to obstacle: move to next obstacle
  - keep track of all intermediate steps with an `X` (???)
* Turn right 90 degrees: maybe a generator of cycle([u, r, d, l])?
* exit_map: return true if no obstacle to the end of the map
* find_obstacle(cur_pos, cur_dir)

* follow_path(cur_pos, cur_dir) until exit_map is true

"""

from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

dname = Path("../../../../resources/2024/")
fname = dname / "d06.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str) -> list[str]:
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = [line.strip() for line in f]
    return content


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


class Position:
    def __init__(self, row: int, col: int):
        "A position defined by (row, column)"
        self.row = row
        self.col = col

    def to_tuple(self):
        """Return position as a tuple"""
        return self.pos

    @property
    def pos(self):
        return (self.row, self.col)

    def __add__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, Position):
            return Position(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return Position(self.row + other[0], self.col + other[1])
        else:
            raise TypeError("Can only add a Position or a tuple of length 2")

    def __iadd__(self, other):
        """Inplace addition `+=`"""
        if isinstance(other, Position):
            self.row += other.row
            self.col += other.col
        elif isinstance(other, tuple) and len(other) == 2:
            self.row += other[0]
            self.col += other[1]
        else:
            raise TypeError("Can only add a Position or a tuple of length 2")

    def __repr__(self):
        """Provide a string representation of the position."""
        return f"Position(row={self.row}, column={self.col})"


class Puzzle:
    DIRECTIONS = ["^", ">", "v", "<"]
    OBSTACLE = "#"
    INCREMENTS = {d: i for d, i in zip(DIRECTIONS, [(-1, 0), (0, 1), (1, 0), (0, -1)])}

    def __init__(self, filename: str):
        "docstring"
        self.labmap = read_data(filename)
        self.cur_pos = self.find_guard()
        self.cur_dir = self.init_dir()
        self.min_row = 0
        self.min_col = 0
        self.max_row = len(self.labmap) - 1
        self.max_col = len(self.labmap[0]) - 1
        self.stops = {direction: [] for direction in self.DIRECTIONS}
        self.counter = 0
        self.new_obstacles = list()
        self.steps = 0
        self.all_steps = 0

    def replace_char(self, s: str, n: int, ch: str = "+"):
        """Replace the char at string index `n` with ch"""
        if n < 0 or n > len(s):
            raise ValueError(f"n ({n}) is out of range")
        if ch not in self.DIRECTIONS + ["-", "|", "+"]:
            pass
        elif s[n] in self.DIRECTIONS:
            ch = s[n]
        elif s[n] in ["-", "|"]:
            ch = "+"
        return s[:n] + ch + s[n + 1 :]

    def guard_pos_in_row(self, row: str):
        """get the guard's position in a row"""
        for guard in self.DIRECTIONS:
            if guard in row:
                return row.index(guard)

    def find_guard(self) -> Position:
        """Get the guard's position"""
        pos = [
            (idx, self.guard_pos_in_row(line))
            for idx, line in enumerate(self.labmap)
            if self.guard_pos_in_row(line)
        ][0]
        return Position(*pos)

    def init_dir(self):
        """Get the initial direction"""
        row, col = self.cur_pos.pos
        return self.labmap[row][col]

    def print_map(self):
        printmap = self.labmap.copy()
        r, c = self.cur_pos.pos
        printmap[r] = self.replace_char(printmap[r], c, self.cur_dir)
        if self.new_obstacles:
            o_r, o_c = self.new_obstacles[-1]
            rprint(self.new_obstacles)
            printmap[o_r] = self.replace_char(printmap[o_r], o_c, "O")
        for line in printmap:
            rprint(line)
        print()

    def exiting(self):
        """True if next step would exit the map"""
        row, col = self.cur_pos.pos
        return (
            (self.cur_dir == "^" and row == self.min_row)
            or (self.cur_dir == ">" and col == self.max_col)
            or (self.cur_dir == "v" and row == self.max_row)
            or (self.cur_dir == "<" and col == self.min_col)
        )

    def next_dir(self):
        """Return the next direction (don't change anything)"""
        idx = self.DIRECTIONS.index(self.cur_dir)
        new_idx = (idx + 1) % 4
        return self.DIRECTIONS[new_idx]

    def turn(self, direction: str = "right"):
        """Update self.cur_dir (only if not exiting)"""
        if self.exiting():
            pass
        else:
            self.cur_dir = self.next_dir()
        r, c = self.cur_pos.pos
        self.labmap[r] = self.replace_char(self.labmap[r], c, ch="+")

    def find_obstacle_up(self):
        """Return the guard's ending position if traveling up"""
        r, c = self.cur_pos.pos
        while r > self.min_row and self.labmap[r - 1][c] != self.OBSTACLE:
            r -= 1
        return (r, c)

    def find_obstacle_right(self):
        """Return the guard's ending position if traveling right"""
        r, c = self.cur_pos.pos
        while c < self.max_col and self.labmap[r][c + 1] != self.OBSTACLE:
            c += 1
        return (r, c)

    def find_obstacle_down(self):
        """Return the guard's ending position if traveling down"""
        r, c = self.cur_pos.pos
        while r < self.max_row and self.labmap[r + 1][c] != self.OBSTACLE:
            r += 1
        return (r, c)

    def find_obstacle_left(self):
        """Return the guard's ending position if traveling left"""
        r, c = self.cur_pos.pos
        while c > self.min_col and self.labmap[r][c - 1] != self.OBSTACLE:
            c -= 1
        return (r, c)

    def add_obstacle(self, obstacle_pos):
        if obstacle_pos in self.stops[self.cur_dir]:
            raise ValueError(
                f"I've been here before! {obstacle_pos=}, {self.cur_dir=}, {self.counter=}"
            )
        else:
            self.stops[self.cur_dir].append(obstacle_pos)

    def find_obstacle(self):

        if self.exiting():
            rprint(f"Exiting (r,c) = {self.cur_pos}, dir={self.cur_dir}")
            end_pos = self.cur_pos
        elif self.cur_dir == "^":
            end_pos = self.find_obstacle_up()
        elif self.cur_dir == ">":
            end_pos = self.find_obstacle_right()
        elif self.cur_dir == "v":
            end_pos = self.find_obstacle_down()
        elif self.cur_dir == "<":
            end_pos = self.find_obstacle_left()
        else:
            raise ValueError(f"invalid direction: {self.cur_dir}")
        if not self.exiting():
            self.counter += 1
        return end_pos

    def count_xs(self):
        """Count the x's in the map"""
        counts = [line.count("x") for line in self.labmap]
        return sum(counts)

    def count_non_dots(self):
        """Count the x's in the map"""
        counts = [
            len(line) - line.count(".") - line.count(self.OBSTACLE)
            for line in self.labmap
        ]
        return sum(counts)

    def would_make_loop(self, pos: tuple):
        """True if a block at the next position would create a loop.

        if traveling up, and the position to the right is a `-`, then
        blocking up a row would take me back to where I've been.

        if traveling right, and the position below is a "|"
        or if traveling down and the position to the left is a "-"
        or if traveling left and the position to the right is a "|"
        """
        cur_row, cur_col = pos
        if self.exiting():
            return
        dir = self.cur_dir
        lab = self.labmap
        new_obstacle = None
        if (
            dir == "^"
            and cur_row > self.min_row
            and cur_col < self.max_col - 1  # Must be able to turn again
            and lab[cur_row][cur_col + 1] in ["+", "-"] + self.DIRECTIONS
            and lab[cur_row - 1][cur_col]
            not in [self.OBSTACLE, "+", "-", "|"] + self.DIRECTIONS
        ):
            new_obstacle = (cur_row - 1, cur_col)
        elif (
            dir == "v"
            and cur_row < self.max_row
            and cur_col > self.min_col + 1  # Must be able to turn again
            and lab[cur_row][cur_col - 1] in ["+", "-"] + self.DIRECTIONS
            and lab[cur_row + 1][cur_col]
            not in [self.OBSTACLE, "+", "-", "|"] + self.DIRECTIONS
        ):
            new_obstacle = (cur_row + 1, cur_col)
        elif (
            dir == ">"
            and cur_col < self.max_col
            and cur_row < self.max_row - 1  # Must be able to turn again
            and lab[cur_row + 1][cur_col] in ["+", "|"] + self.DIRECTIONS
            and lab[cur_row][cur_col + 1]
            not in [self.OBSTACLE, "+", "-", "|"] + self.DIRECTIONS
        ):
            new_obstacle = (cur_row, cur_col + 1)
        elif (
            dir == "<"
            and self.steps > 0  # Don't look at the direction you just came from
            and cur_col > self.min_col
            and cur_row > self.min_row + 1  # Must be able to turn again
            and lab[cur_row - 1][cur_col] in ["+", "|"] + self.DIRECTIONS
            and lab[cur_row][cur_col - 1]
            not in [self.OBSTACLE, "+", "-", "|"] + self.DIRECTIONS
        ):
            # if self.all_steps > 14:
            #     rprint(f"{cur_row=}, {cur_col=}")

            new_obstacle = (cur_row, cur_col - 1)
        if new_obstacle:
            self.new_obstacles.append(new_obstacle)

        return new_obstacle

    def check_for_loop(self, pos: tuple):
        row, col = pos
        return (row, col)

    def find_loop_pos(self, start_pos: tuple, end_pos: tuple) -> tuple:
        """Find a loop position between cur_pos and end_pos"""
        dir = self.cur_dir
        lab = self.labmap
        row, col = start_pos
        end_row, end_col = end_pos
        loop_pos = None

        if dir == "^" and end_row <= row:
            loop_pos = self.check_for_loop((row, col))
            # Check if there is a block position to the righ
            # That we've seen
            if loop_pos:
                pass
        return loop_pos


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    puzzle = Puzzle(filename)

    while not puzzle.exiting():
        end_pos = puzzle.find_obstacle()

    return puzzle.count_non_dots()


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2


rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    puzzle = Puzzle(filename)
    while not puzzle.exiting():
        end_pos = puzzle.find_obstacle()
        loop_pos = puzzle.find_loop_pos(puzzle.cur_pos, end_pos=end_pos)
        new_obstacle = puzzle.would_make_loop(end_pos)

    # puzzle.print_map()
    rprint(puzzle.new_obstacles)
    return puzzle.count_non_dots()


rprint(f"""test data: {part2(FNAME_TEST)}""")
# rprint(f"""Problem input: {part2(fname)}""")
