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

import logging
from rich.logging import RichHandler

# Set up basic config for logging
FORMAT = "%(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def read_data(filename: str) -> list[str]:
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = [line.strip() for line in f]
    return content


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


class Position:
    """A position object"""

    def __init__(self, row: int, col: int):
        "A position defined by (row, column)"
        self.row = row
        self.col = col

    def to_tuple(self):
        """Return position as a tuple"""
        return self.pos

    @property
    def pos(self):
        """Return the current position as a tuple"""
        return (self.row, self.col)

    def __add__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, Position):
            return Position(self.row + other.row, self.col + other.col)
        if isinstance(other, tuple) and len(other) == 2:
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

    def lt(self, other, direction: tuple[int, int]) -> bool:
        """Compare to positions based on a direction vector.
        Uses a projection on the direction vector."""

        if isinstance(other, Position):
            other_row, other_col = other.row, other.col
        elif isinstance(other, tuple) and len(direction) == 2:
            other_row, other_col = other
        else:
            raise TypeError("Can only compare with another Position or a tuple")

        # Compute dot product with direction for comparison
        projection_self = self.row * direction[0] + self.col * direction[1]
        projection_other = other_row * direction[0] + other_col * direction[1]

        return projection_self < projection_other

    def __repr__(self):
        """Provide a string representation of the position."""
        return f"Position(row={self.row}, column={self.col})"


class Puzzle:
    """The puzzle and all its methods"""

    DIRECTIONS = ["^", ">", "v", "<"]
    OBSTACLE = "#"
    INCREMENTS = dict(zip(DIRECTIONS, [(-1, 0), (0, 1), (1, 0), (0, -1)]))

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
        self.new_obstacles = []
        self.steps = 0
        self.all_steps = 0

    @property
    def incr(self):
        """Get the increment vector given the current direction"""
        return self.INCREMENTS[self.cur_dir]

    def replace_char(self, s: str, n: int, ch: str):
        """Replace the char at string index `n` with ch"""
        if n < 0 or n >= len(s):
            raise ValueError(f"n ({n}) is out of range")
        return s[:n] + ch + s[n + 1 :]

    def guard_pos_in_row(self, row: str):
        """get the guard's position in a row"""
        res = None
        for guard in self.DIRECTIONS:
            if guard in row:
                res = row.index(guard)
                logger.debug(f"guard pos {guard} = {res}")
                return res

    def find_guard(self) -> Position:
        """Get the guard's position"""
        pos = [
            (idx, self.guard_pos_in_row(line))
            for idx, line in enumerate(self.labmap)
            if self.guard_pos_in_row(line) is not None
        ][0]
        logger.debug(f"{pos=}")
        # breakpoint()

        return Position(*pos)

    def init_dir(self):
        """Get the initial direction"""
        row, col = self.cur_pos.pos
        return self.labmap[row][col]

    def print_map(self):
        """Print out the map (for debugging)"""
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

    def draw_map(self, pos: Position = None, filename: str = None):
        """Draw map with new obstacles"""
        printmap = self.labmap.copy()
        posit = pos if pos else self.cur_pos
        r, c = posit.pos
        new_obs = self.new_obstacles  # list[tuple]
        for row, col in new_obs:
            printmap[row] = self.replace_char(printmap[row], col, "O")
        if filename:
            with open(filename, "w") as f:
                for line in printmap:
                    f.write(line + "\n")

        else:
            for line in printmap:
                rprint(line)
        print()

    def exiting(self, pos: Position = None, direction: str = None):
        """True if next step would exit the map"""
        row, col = pos.pos if pos else self.cur_pos.pos
        direc = direction if direction else self.cur_dir
        return (
            (direc == "^" and row == self.min_row)
            or (direc == ">" and col == self.max_col)
            or (direc == "v" and row == self.max_row)
            or (direc == "<" and col == self.min_col)
        )

    def next_dir(self, direction: str = None):
        """Return the next direction (don't change anything)"""
        direc = direction if direction else self.cur_dir
        idx = self.DIRECTIONS.index(direc)
        new_idx = (idx + 1) % 4
        return self.DIRECTIONS[new_idx]

    def turn(self):
        """Update self.cur_dir (only if not exiting)"""
        if self.exiting():
            pass
        else:
            self.cur_dir = self.next_dir()
        r, c = self.cur_pos.pos
        self.labmap[r] = self.replace_char(self.labmap[r], c, ch=self.cur_dir)

    def find_obstacle_up(self, pos: Position = None) -> Position:
        """Return the guard's ending position if traveling up"""
        r, c = pos.pos if pos else self.cur_pos.pos
        incr_r, incr_c = (-1, 0)
        while r > self.min_row and self.labmap[r + incr_r][c + incr_c] != self.OBSTACLE:
            r += incr_r
            c += incr_c
        return Position(r, c)

    def find_obstacle_right(self, pos: Position = None) -> Position:
        """Return the guard's ending position if traveling right"""
        # r, c = self.cur_pos.pos
        r, c = pos.pos if pos else self.cur_pos.pos
        incr_r, incr_c = (0, 1)
        while c < self.max_col and self.labmap[r + incr_r][c + incr_c] != self.OBSTACLE:
            r += incr_r
            c += incr_c
        return Position(r, c)

    def find_obstacle_down(self, pos: Position = None) -> Position:
        """Return the guard's ending position if traveling down"""
        # r, c = self.cur_pos.pos
        r, c = pos.pos if pos else self.cur_pos.pos
        incr_r, incr_c = (1, 0)
        while r < self.max_row and self.labmap[r + incr_r][c + incr_c] != self.OBSTACLE:
            r += incr_r
            c += incr_c
        return Position(r, c)

    def find_obstacle_left(self, pos: Position = None) -> Position:
        """Return the guard's ending position if traveling left"""
        # r, c = self.cur_pos.pos
        r, c = pos.pos if pos else self.cur_pos.pos
        incr_r, incr_c = (0, -1)
        while c > self.min_col and self.labmap[r + incr_r][c + incr_c] != self.OBSTACLE:
            r += incr_r
            c += incr_c
        return Position(r, c)

    def obstacle_exists(self, obstacle_pos: Position) -> bool:
        """True if we've seen this obstacle before"""
        return obstacle_pos.pos in self.stops[self.cur_dir]

    def add_obstacle(self, obstacle_pos: Position):
        """Add the obstacle to the current list of stops"""
        if not self.obstacle_exists(obstacle_pos):
            self.stops[self.cur_dir].append(obstacle_pos.pos)

    def find_obstacle(self, pos: Position = None, direction=None) -> Position:
        """Find an obstacle in a given direction"""
        direc = direction if direction else self.cur_dir
        start_pos = pos if pos else self.cur_pos
        if self.exiting():
            rprint(f"Exiting (r,c) = {start_pos}, dir={direc}")
            end_pos = start_pos
        elif direc == "^":
            end_pos = self.find_obstacle_up(start_pos)
        elif direc == ">":
            end_pos = self.find_obstacle_right(start_pos)
        elif direc == "v":
            end_pos = self.find_obstacle_down(start_pos)
        elif direc == "<":
            end_pos = self.find_obstacle_left(start_pos)
        else:
            raise ValueError(f"invalid direction: {direc}")
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

    def find_all_loop_spots(self, start_pos, end_pos) -> Position:
        """Find all loops spot between start/end pos
        Check to see if we've seen this obstacle OR the following one.
        It may be enough to just check the following one...
        """
        next_dir = self.next_dir()
        next_dir2 = self.next_dir(next_dir)
        incr = self.incr
        next_pos = start_pos + incr
        # Stop before end_pos, so you don't add an obstacle over an existing one.
        while next_pos.lt(other=end_pos, direction=incr):
            # rprint(f"checking {next_pos}, in direction {next_dir}")
            obstacle = self.find_obstacle(pos=next_pos, direction=next_dir)
            obstacle2 = self.find_obstacle(pos=obstacle, direction=next_dir2)
            if self.exiting(pos=obstacle, direction=next_dir):
                pass
            else:
                # rprint(f"obstacle found {obstacle}")
                if obstacle2.pos in self.stops[next_dir2]:
                    # found a possible loop (1 place past current spot)
                    loop_obstacle_pos = next_pos + incr
                    rprint(f"loop obstacle location found: {loop_obstacle_pos}")
                    self.new_obstacles.append(loop_obstacle_pos.pos)
            next_pos = next_pos + incr


# ########## Part 2


rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    puzzle = Puzzle(filename)
    rprint("starting")
    puzzle.draw_map(filename="map_starting.txt")
    while not puzzle.exiting():
        start_pos = puzzle.cur_pos
        end_pos = puzzle.find_obstacle()
        logger.debug(f"{end_pos=} (exiting? {puzzle.exiting(end_pos)})")
        if puzzle.obstacle_exists(end_pos):
            rprint(f"You've entered a loop at {end_pos=}")
            break
        puzzle.add_obstacle(end_pos)
        puzzle.find_all_loop_spots(start_pos, end_pos)
        # puzzle.draw_map()
        puzzle.cur_pos = end_pos
        puzzle.turn()
        # rprint(f"Bottom of while loop {puzzle.cur_pos}")

        # loop_pos = puzzle.find_loop_pos(puzzle.cur_pos, end_pos=end_pos)
        # new_obstacle = puzzle.would_make_loop(end_pos)

    puzzle.draw_map(filename="outmap.txt")
    # puzzle.print_map()
    distinct_new_obstacles = set(puzzle.new_obstacles)
    return len(distinct_new_obstacles)
    # return puzzle.count_non_dots()


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""test data: {part2("test_data_4.txt")}""")

# rprint(f"""Problem input: {part2(fname)}""")

# Tries:
# Too low
# Problem input: 390
# Problem input: 669
#
# Too high


# test_data_missing_loop.txt showed that you can turn
# towards an obstacle that you haven't seen before,
# and still cause a loop.

# Instead of checking to see if I've seen a new_stop before,
# See if I've seen the NEXT obstacle after that.

# Also, exit if I enter a loop.
