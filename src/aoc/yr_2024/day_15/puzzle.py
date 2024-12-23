#!/usr/bin/env python

import logging
from pathlib import Path

import rich
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import flatten

# from aoc.pyutils.utils import flatten, time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d15.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str) -> (list[list[str]], str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        grid = []
        line = f.readline().strip()
        while line:
            grid.append(list(line))
            line = f.readline().strip()
        moves = list(f.read().replace("\n", ""))
        return grid, moves


def widen_line(line: list[str]) -> list[str]:
    """widen all cells except robot"""
    new_vals = {"#": ["#", "#"], "O": ["[", "]"], ".": [".", "."], "@": ["@", "."]}
    return flatten([new_vals[cell] for cell in line])


def widen_grid(grid: list[list[str]]) -> list[list[str]]:
    """widen the entire grid"""
    return [widen_line(line) for line in grid]


Point = tuple[int, int]  # (row, col)


class Part1(BaseModel):
    grid: list[list[str]] = Field(
        description="the grid, as a list of strings, (each row is a string)"
    )
    moves: list[str] = Field(
        description="A single string containing the list of move (^,>,v,<)"
    )
    robot: Point | None = Field(default=None, description="the location of the robot")
    current_move_index: int = Field(
        default=0, description="Index of the next move in the move str"
    )

    BLOCK: str = "O"
    WALL: str = "#"
    FREE_SPACE: str = "."
    move_incr: dict = {
        "^": (-1, 0),  # Up
        ">": (0, 1),  # Right
        "v": (1, 0),  # Down
        "<": (0, -1),  # Left
    }

    def find_chars(self, s: list[str], char: str = FREE_SPACE) -> list[int]:
        "Find the indices of all `char` in `s`"
        assert len(char) == 1
        return [i for i, c in enumerate(s) if c == char]

    @model_validator(mode="after")
    @classmethod
    def find_robot(cls, model) -> "Part1":
        """Compute the robot position if not explicitly set.
        Find the `@`"""
        if model.robot is None:  # Only compute if not provided
            model.robot = [
                (row, line.index("@"))
                for row, line in enumerate(model.grid)
                if "@" in line
            ][0]
        return model

    @field_validator("moves")
    @classmethod
    def validate_moves(cls, value: str) -> str:
        "Ensure moves only contains ^, >, v, <"
        if not all(c in "^>v<" for c in value):
            raise ValueError(
                "Invalid moves in 'move_str'. Only the characters '^', '>', 'v', and '<' are allowed."
            )
        return value

    def gval(self, point: Point) -> str:
        """Get the value of grid at point"""
        row, col = point
        return self.grid[row][col]

    def draw(self):
        """Draw the grid"""
        print()
        rich.print("\n".join(["".join(line) for line in self.grid]))
        print()

    @property
    def direction(self) -> str:
        return self.moves[self.current_move_index]

    @property
    def next_move(self) -> str:
        """Get the next direction, without changing the move counter"""
        if self.current_move_index >= len(self.moves):
            raise ValueError(f"Move index {self.current_move_index} is out of range")
        return self.moves[self.current_move_index + 1]  # type: ignore

    def update_point(self, point: Point, char: str) -> None:
        row, col = point
        self.grid[row][col] = char

    def next_robot_position(self):
        """Get the position adjacent to robot in move dir"""
        drow, dcol = self.move_incr[self.direction]
        rrow, rcol = self.robot
        return (rrow + drow, rcol + dcol)

    def find_next_open(self):
        """Return the next possible space to move to in the move dir"""
        drow, dcol = self.move_incr[self.direction]
        row, col = self.robot
        # next_point = self.next_robot_position((row, col))
        while 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            row += drow
            col += dcol
            if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
                return None  # Out of bounds
            cell = self.gval((row, col))
            if cell == self.FREE_SPACE:
                return row, col
            if cell == self.WALL:
                return None  # Hit a wall
        return None  # no open space found

    def robot_clear(self):
        """True if the robot can move w/o moving boxes"""
        return "." == self.gval(self.robot)

    def can_move(self) -> bool:
        """True if the next space is empty, or the boxes can be moved"""

    def swap(self, start_pos, end_pos):
        """Swap the grid value at start/end positions
        End position should be a FREE_SPACE"""
        start_val = self.gval(start_pos)
        end_val = self.gval(end_pos)
        if end_val != self.FREE_SPACE:
            raise ValueError(f"End destination must be a FREE_SPACE {end_pos}")
        self.update_point(end_pos, start_val)
        self.update_point(start_pos, end_val)

    def move(self, draw=False):
        """Move the robot"""
        # breakpoint()

        next_open_posit = self.find_next_open()
        if next_open_posit is None:
            pass
        else:
            next_adj = self.next_robot_position()
            if next_open_posit != next_adj:
                self.swap(next_adj, next_open_posit)  # move box to end of boxes
            self.swap(self.robot, next_adj)  # move robot
            self.robot = next_adj
        self.current_move_index += 1
        if self.current_move_index < len(self.moves):
            self.update_point(self.robot, self.direction)
        if draw:
            self.draw()

    def move_all(self):
        """Execute all moves"""
        num_moves = len(self.moves)
        for i in range(num_moves):
            self.move()
        print(f"move number {i}")
        self.draw()

    def find_all_boxes(self):
        """Find the grid positions of all boxes"""
        box_coords = []
        for ridx, row in enumerate(self.grid):
            for cidx, cell in enumerate(row):
                if cell == self.BLOCK:
                    box_coords.append((ridx, cidx))
        return box_coords

    def calc_gps(self, point: Point):
        """100 x row + 1 * col"""
        row, col = point
        return 100 * row + col

    def total_gps(self):
        boxes = self.find_all_boxes()
        return sum(map(self.calc_gps, boxes))

    def execute_1(self):
        self.move_all()
        return self.total_gps()


# ########## Part 1


def exec_part1():
    rich.print(Rule("Part 1", style="bold green"))
    rich.print(Panel.fit("[bold green]Part 1"))  #

    grid, moves = read_data(filename="test_data.txt")
    # p1 = Part1(grid=grid, moves=moves)
    rich.print(f"test data, part1: {Part1(grid=grid, moves=moves).execute_1()}")

    grid, moves = read_data(filename=fname)
    rich.print(f"puzzle data, part1: {Part1(grid=grid, moves=moves).execute_1()}")


# exec_part1()

# # ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


class Part2(Part1):
    """Differences from Part1
    1. if moving block left, swap left block, then right block, then robot
    2. if moving block right, swap right, then left then robot
    3. If moving up/down, need to see how wide the blocks are,
       since they can overlap
    """

    def shift_robot_blocks_horiz(self, end_posit: Point):
        """Shift the robot and blocks horizontally
        if the robot is in col c, and end posit is col e,
        shift everything between c and e over a space.

        ##.#.[][]@[].##  <-- start
        012345678901234

        ##.#[][]@.[].##  <-- ending

        c=9, e=4
        line[:e] + line[e+1:c+1] + [line[e]] + line[c+1:]
        '##.#[][]@.[].##'

        What if shifting right?

        c=9, e=12
        line[:c] + [line[e]] + line[c:e] + line[e+1:]
        '##.#.[][].@[]##'
        """
        row, col = self.robot
        end_row, end_col = end_posit
        if row != end_row:
            raise ValueError("row and end_row must be the same for horiz shifting")

        line = self.grid[row]
        if col > end_col:
            new_line = (
                line[:end_col]  # to the left of space
                + line[end_col + 1 : col + 1]  # blocks + robot
                + [line[end_col]]  # space
                + line[col + 1 :]  # to the right of robot
            )
        else:
            new_line = (
                line[:col] + [line[end_col]] + line[col:end_col] + line[end_col + 1 :]
            )
        self.grid[row] = new_line

    def move(self, draw=True):
        # robot moves 1 space in any direction
        next_adj = self.next_robot_position()
        next_open_position = self.find_next_open()
        if self.direction in ["<", ">"]:
            # Horizontal moves are essentially the same, just a shift 1 block left/right
            next_open_position = self.find_next_open()
            if next_open_position is None:
                pass
            else:
                self.shift_robot_blocks_horiz(next_open_position)
                self.robot = next_adj
        elif next_adj == next_open_position:
            # Vertical moves are move complicated due to overlap
            # robot can move w/o obstruction
            self.swap(self.robot, next_adj)
            self.robot = next_adj
        else:
            # Vertical moves with blocks are move complicated due to overlap
            pass
        self.current_move_index += 1
        if self.current_move_index < len(self.moves):
            self.update_point(self.robot, self.direction)
        if draw:
            self.draw()


grid, moves = read_data(filename="test_data.txt")
grid = widen_grid(grid)
p1 = Part2(grid=grid, moves=moves)

# rich.print(f"test data, part2: {Part1(grid=grid, moves=moves).execute_1()}")


# @time_it
# def part2(filename: str) -> int:
#     """Run part 2 given the input file
#     Return value should be the solution"""


# # rprint(f"""test data: {part2(FNAME_TEST)}""")
# rprint(f"""Problem input: {part2(fname)}""")
