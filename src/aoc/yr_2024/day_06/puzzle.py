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


def replace_char(s: str, n: int, ch: str = "x"):
    """Replace the char at string index `n` with ch"""
    if n < 0 or n > len(s):
        breakpoint()
        raise ValueError(f"n ({n}) is out of range")
    return s[:n] + ch + s[n + 1 :]


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


class Puzzle:
    DIRECTIONS = ["^", ">", "v", "<"]
    OBSTACLE = "#"

    def __init__(self, filename: str):
        "docstring"
        self.labmap = read_data(filename)
        self.cur_pos = self.find_guard()
        self.cur_dir = self.init_dir()
        self.min_row = 0
        self.min_col = 0
        self.max_row = len(self.labmap) - 1
        self.max_col = len(self.labmap[0]) - 1
        self.stops_up = []
        self.stops_right = []
        self.stops_down = []
        self.stops_left = []
        self.counter = 0

    def guard_pos_in_row(self, row: str):
        """get the guard's position in a row"""
        for guard in self.DIRECTIONS:
            if guard in row:
                return row.index(guard)

    def find_guard(self):
        """Get the guard's position"""
        return [
            (idx, self.guard_pos_in_row(line))
            for idx, line in enumerate(self.labmap)
            if self.guard_pos_in_row(line)
        ][0]

    def init_dir(self):
        """Get the initial direction"""
        r, c = self.cur_pos
        return self.labmap[r][c]

    def exiting(self):
        """True if next step would exit the map"""
        r, c = self.cur_pos
        return (
            (self.cur_dir == "^" and r == self.min_row)
            or (self.cur_dir == ">" and c == self.max_col)
            or (self.cur_dir == "v" and r == self.max_row)
            or (self.cur_dir == "<" and c == self.min_col)
        )

    def turn(self, direction: str = "right"):
        """Dont change the direction if exiting"""
        idx = self.DIRECTIONS.index(self.cur_dir)
        if self.exiting():
            new_idx = idx
        elif direction == "right":
            new_idx = (idx + 1) % 4
        else:
            raise ValueError(f"Bad direction: {direction}")
        self.cur_dir = self.DIRECTIONS[new_idx]

    def find_obstacle_up(self):
        """Return the guard's ending position if traveling up"""
        r, c = self.cur_pos
        starting_map = self.labmap.copy()
        while r > self.min_row and self.labmap[r - 1][c] != self.OBSTACLE:
            r -= 1
            starting_map[r] = replace_char(starting_map[r], c)
            self.labmap = starting_map.copy()
        self.cur_pos = (r, c)
        if (r, c) in self.stops_up:
            raise ValueError(
                f"I'be been here before! {self.cur_pos=}, {self.cur_dir=}, {self.counter=}"
            )
        else:
            self.stops_up.append((r, c))
        self.turn()
        return self.cur_pos

    def find_obstacle_right(self):
        """Return the guard's ending position if traveling right"""
        r, c = self.cur_pos
        starting_map = self.labmap.copy()
        while c < self.max_col and self.labmap[r][c + 1] != self.OBSTACLE:
            c += 1
            starting_map[r] = replace_char(starting_map[r], c)
        self.labmap = starting_map.copy()
        self.cur_pos = (r, c)
        if (r, c) in self.stops_right:
            raise ValueError(
                f"I'be been here before! {self.cur_pos=}, {self.cur_dir=}, {self.counter=}"
            )
        else:
            self.stops_up.append((r, c))
        self.turn()
        return self.cur_pos

    def find_obstacle_down(self):
        """Return the guard's ending position if traveling down"""
        r, c = self.cur_pos
        starting_map = self.labmap.copy()
        while r < self.max_row and self.labmap[r + 1][c] != self.OBSTACLE:
            r += 1
            starting_map[r] = replace_char(starting_map[r], c)
        self.labmap = starting_map.copy()
        self.cur_pos = (r, c)
        if (r, c) in self.stops_down:
            raise ValueError(
                f"I'be been here before! {self.cur_pos=}, {self.cur_dir=}, {self.counter=}"
            )
        else:
            self.stops_up.append((r, c))
        self.turn()
        return self.cur_pos

    def find_obstacle_left(self):
        """Return the guard's ending position if traveling left"""
        r, c = self.cur_pos
        starting_map = self.labmap.copy()
        while c > self.min_col and self.labmap[r][c - 1] != self.OBSTACLE:
            c -= 1
            starting_map[r] = replace_char(starting_map[r], c)
        self.labmap = starting_map.copy()
        self.cur_pos = (r, c)
        if (r, c) in self.stops_left:
            raise ValueError(
                f"I'be been here before! {self.cur_pos=}, {self.cur_dir=}, {self.counter=} "
            )
        else:
            self.stops_up.append((r, c))
        self.turn()
        return self.cur_pos

    def print_map(self):
        printmap = self.labmap.copy()
        r, c = self.cur_pos
        printmap[r] = replace_char(printmap[r], c, self.cur_dir)
        for line in printmap:
            rprint(line)
        print()

    def find_obstacle(self):
        if self.counter > 138:
            breakpoint()

        if self.exiting():
            rprint(f"Exiting (r,c) = {self.cur_pos}, dir={self.cur_dir}")
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
            rprint(
                Rule(
                    f"Obstacle {self.counter}, (r,c) = {self.cur_pos}, next dir={self.cur_dir}",
                    style="bold red",
                )
            )
            # self.print_map()
        return end_pos

    def count_xs(self):
        """Count the x's in the map"""
        counts = [line.count("x") for line in self.labmap]
        return sum(counts)


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    puzzle = Puzzle(filename)
    # puzzle.print_map()
    # Test turning
    # rprint(f"{puzzle.cur_dir=}")
    # for _ in range(4):
    #     puzzle.turn()
    #     rprint(f"turn to {puzzle.cur_dir=}")

    # first_obstacle = puzzle.find_obstacle()
    # rprint(f"{first_obstacle=}")
    # puzzle.print_map()
    # second_obstacle = puzzle.find_obstacle()
    # rprint(f"{second_obstacle=}")
    # puzzle.print_map()
    # third_obstacle = puzzle.find_obstacle()
    # rprint(f"{third_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()
    # fourth_obstacle = puzzle.find_obstacle()
    # rprint(f"{fourth_obstacle=}")
    # puzzle.print_map()

    while not puzzle.exiting():
        puzzle.find_obstacle()

    # puzzle.print_map()
    return puzzle.count_xs()


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
