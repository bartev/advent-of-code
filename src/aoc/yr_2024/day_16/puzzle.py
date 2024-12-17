#!/usr/bin/env python

"""
Cost:
forward motion: 1 point
right turn: 1000 points

Find the lease expensive path
"""
import heapq
import logging
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d16.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        grid = [line.strip() for line in f.readlines()]
    return grid


Point = tuple[int, int]  # (row, col)
Grid = list[str]


def next_directions(prev_dir) -> list[Point]:
    """prev_dir is an index (0-4)
    Return a list of next directions"""


def dijkstra_maze(maze: Grid, start: Point, end: Point, direc="e"):
    # maze dimensions
    rows, cols = len(maze), len(maze[0])

    # Directions and their indices (up, right, down, left)
    # directions n, s, e, w
    direc_incrs = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (-1, 0)}
    directions = direc_incrs.keys()

    # directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # direction_indices = {(-1, 0): 0, (0, 1): 1, (1, 0): 2, (0, -1): 3}

    # Priority queue
    # (current_cost, current_position, previous_direction_index)
    # I should never move 180 degrees

    queue = [(0, start, direc)]  # Initialize the queue with start position, 0 cost
    costs = {start: 0}  # Dict to store minimum costs to each cell

    while queue:
        # get the lowest cost item from the queue
        current_cost, (x, y), prev_dir = heapq.heappop(queue)

        if (x, y) == end:
            return current_cost  # lowest cost seen to date

        # Explore neighboors
        for new_dir in directions:
            dx, dy = direc_incrs[new_dir]
            new_x, new_y = x + dx, y + dy
            # new_dir = direction_indices[direc]

            # check bounds and if the cell is traversable
            if (
                0 <= new_x < rows
                and 0 <= new_y < cols
                and maze[new_x][new_y] in ["S", "E", "."]
            ):
                # Calculate cost of this move
                move_cost = 1 if prev_dir == new_dir else 1000
                # new_cost is the cost if I moved into this space
                new_cost = current_cost + move_cost

                # Update coste and queue if this path is cheaper
                if (new_x, new_y) not in costs or new_cost < costs[(new_x, new_y)]:
                    costs[(new_x, new_y)] = new_cost
                    heapq.heappush(queue, (new_cost, (new_x, new_y), new_dir))
    return None


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    maze = read_data(filename)
    rich.print(maze)

    nrows = len(maze)
    ncols = len(maze[0])
    start_pos = (nrows - 2, 1)
    end_pos = (1, ncols - 2)

    cost = dijkstra_maze(maze=maze, start=start_pos, end=end_pos, direc="e")
    return cost


rich.print(f"""test data: {part1(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


# @time_it
# def part2(filename: str) -> int:
#     """Run part 2 given the input file
#     Return value should be the solution"""


# rich.print(f"""test data: {part2(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part2(fname)}""")
