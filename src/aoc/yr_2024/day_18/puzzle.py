#!/usr/bin/env python

import csv
import heapq
import logging
from pathlib import Path

import rich
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.grid_points import Grid, Point
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d18.txt"
FNAME_TEST = "test_data.txt"


def read_csv_data(filename: str):
    """Read the (x, y) data in the file into Points (y, x)"""
    with open(filename, "r", encoding="utf8") as f:
        reader = csv.reader(f)
        tuples_list = []
        for row in reader:
            (col, row) = map(int, row)
            tuples_list.append((row, col))
    return tuples_list


# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


class PGrid(Grid):
    """Grid for this puzzle
    Points are in (row, col), puzzle input is in (col, row)"""

    def __init__(self, dim: int):
        "Setup up a square grid of dim x dim"
        super().__init__(rows=dim, cols=dim)

    def set(self, point: Point):
        """Overwrite the `set` method to put a `#` on the point"""
        super().set(point, "#")


def dijkstra(maze: Grid):
    """Solve for shortest path (unweighted) to the end of the grid
    Start at (0,0), end at (rows, cols).
    """
    # maze dimensions
    rows, cols = len(maze), len(maze[0])

    # Start, end positions
    start = (0, 0)
    end = (rows - 1, cols - 1)

    # Directions and their indices (up, right, down, left)
    # directions n, s, e, w
    direc_incrs = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (0, -1)}
    directions = direc_incrs.keys()

    queue = [(0, start)]  # Initialize the queue with start position, 0 cost
    costs = {start: 0}  # Dict to store minimum costs to each cell
    parent = {start: None}

    while queue:
        # Get the lowest cost item from the queue
        current_cost, (y, x) = heapq.heappop(queue)
        # breakpoint()

        # Stop when I first get to end (this is the fastest way)
        if (y, x) == end:
            return current_cost

        # Explore neighbors
        for new_dir in directions:
            dy, dx = direc_incrs[new_dir]
            new_y, new_x = y + dy, x + dx
            new_point = (new_y, new_x)

            # Check bounds and if cell is traversable
            if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_x][new_y] == ".":
                # Increament cost
                new_cost = current_cost + 1

                # Update cost and queue if this path is cheaper
                if new_point not in costs or new_cost < costs[new_point]:
                    costs[new_point] = new_cost
                    parent[new_point] = (y, x)
                    heapq.heappush(queue, (new_cost, new_point))

    # rich.print(f"{queue=}")
    # rich.print(f"{costs=}")
    return -1


@time_it
def part1(filename: str, max_grid_dim: int = 70, num_bytes: int = 1024) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    moves = read_csv_data(filename)
    maze = PGrid(max_grid_dim + 1)
    for i in range(num_bytes):
        maze.set(moves[i])

    # maze.print_grid()

    cost = dijkstra(maze.grid)
    return cost


rich.print(f"""test data: {part1(FNAME_TEST, max_grid_dim=6, num_bytes=12)}""")
rich.print(f"""Problem input: {part1(fname,  max_grid_dim=70, num_bytes=1024)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


def binary_search(grid_dim: int, moves: list[Point]) -> Point:
    """Find first move that causes maze to be unsolvable
    invariants
    idx_start: is solvable
    idx_end: is under test

    """
    idx_start = 0
    idx_end = len(moves)

    found = False

    idx_half = (idx_start + idx_end) // 2
    while not found:
        # Check the 1/2 point
        # breakpoint()

        # initialize a new maze
        maze = PGrid(grid_dim + 1)
        # Add drops up to idx_end
        for i in range(idx_half):
            maze.set(moves[i])

        cost = dijkstra(maze.grid)
        if cost < 0:
            # not solvable maze, adjust the end closer
            idx_end = idx_half
        else:
            # solvable, adjust start
            idx_start = idx_half

        new_idx_half = (idx_start + idx_end) // 2
        if idx_half == new_idx_half:
            found = True
        else:
            idx_half = new_idx_half
            print(f"binary search: {idx_start, idx_end, idx_half}")

    return moves[idx_half]


@time_it
def part2(filename: str, max_grid_dim: int = 70) -> int:
    """Run part 2 given the input file
    Return value should be the solution
    Run a binary search on the number of items to drop
    """
    moves = read_csv_data(filename)
    row, col = binary_search(grid_dim=max_grid_dim, moves=moves)
    return col, row


rich.print(f"""test data: {part2(FNAME_TEST, max_grid_dim=6)}""")
rich.print(f"""Problem input: {part2(fname, max_grid_dim=70)}""")
