#!/usr/bin/env python

import logging
from collections import deque
from functools import cache
from itertools import product
from pathlib import Path

import rich
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

dname = Path("../../../../resources/2024/")
fname = dname / "d21.txt"
FNAME_TEST = "test_data.txt"


console = Console()


def read_data(filename: str) -> list[str]:
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        content = [line.strip() for line in f.readlines()]
    return content


# read_data('test_data.txt')

# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


Point = tuple[int, int]

numeric_keypad = {
    # "gap": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}

arrow_keypad = {
    # "gap": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def dpoint(start: str, end: str, keypad) -> Point:
    """Find the moves needed to go from start to end in terms of ^, >, v, <"""
    start_row, start_col = keypad[start]
    end_row, end_col = keypad[end]
    d_row, d_col = end_row - start_row, end_col - start_col
    x_char = "<" if d_col < 0 else ">" if d_col > 0 else ""
    y_char = "^" if d_row < 0 else "v" if d_row > 0 else ""
    if end_col == 0:  # Avoid the empty space in col 1
        # move to right row first
        move_str = y_char * abs(d_row) + x_char * abs(d_col)
    else:
        # move to right column first
        move_str = x_char * abs(d_col) + y_char * abs(d_row)
    return move_str + "A"


def process_doorcode(code: str):
    """Process a single doorcode
    Get arrow codes to press the numbers on the numeric keypad
    code is like '029A'
    """
    # from_a = "A" + code
    key_paths_1 = zip("A" + code, code)
    robot_1_buttons = "".join(
        [dpoint(start, end, numeric_keypad) for start, end in key_paths_1]
    )
    key_paths_2 = zip("A" + robot_1_buttons, robot_1_buttons)
    robot_2_buttons = "".join(
        [dpoint(start, end, arrow_keypad) for start, end in key_paths_2]
    )
    key_paths_3 = zip("A" + robot_2_buttons, robot_2_buttons)
    my_buttons = "".join(
        [dpoint(start, end, arrow_keypad) for start, end in key_paths_3]
    )
    return robot_1_buttons, robot_2_buttons, my_buttons


def bfs_shortest_paths(start: Point, end: Point, keypad: dict[str, Point]) -> list[str]:
    """Find all the shortest paths between 2 points on a grid, avoiding the gap"""
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    # reverse_directions = {v: k for k, v in directions.items()}
    queue = deque([(start, "")])
    visited = {}
    shortest_paths = []
    min_length = float("inf")
    keypad_bounds = set(keypad.values())

    logger.debug(f"Now searching {start} - {end}")
    while queue:
        current, path = queue.popleft()
        # breakpoint()

        if len(path) > min_length:  # Stop if longer than the shortest found
            continue

        if current == end:
            if len(path) < min_length:
                min_length = len(path)
                shortest_paths = [path]
                logger.debug(f"new shortest path: {path}")
            elif len(path) == min_length:
                shortest_paths.append(path)
                logger.debug(f"appending to shortest path: {path}")
            continue
        for move, (drow, dcol) in directions.items():
            next_pos = (current[0] + drow, current[1] + dcol)
            if next_pos in keypad_bounds:  # Stay within the keypad boundaries
                next_path = path + move
                distance = len(next_path)
                # only explore if not visited or we found another shortest path
                if next_pos not in visited or distance <= visited[next_pos]:
                    visited[next_pos] = distance
                    queue.append((next_pos, next_path))
    # breakpoint()

    return shortest_paths


@cache
def bfs_dpoint(start: str, end: str, keypad_name: str) -> list[str]:
    """Find all shortest paths between 2 keys"""
    keypad = numeric_keypad if keypad_name == "numeric" else arrow_keypad
    return bfs_shortest_paths(keypad[start], keypad[end], keypad)


def stringify_paths(path_list: list[str]):
    """Join a list of paths with A into a single string"""
    return ["A".join(path) for path in product(*path_list)]


def flatten_remove_dupes(nested_list: list[list]) -> list:
    """Flatten 1 level of a nested list"""
    return list(set([item for sublist in nested_list for item in sublist]))


def bfs_process_doorcode(code: str):
    """Process a single doorcode with BFS"""
    # Get all paths for robot 1
    key_paths_1 = zip("A" + code, code)
    robot_1_buttons = [bfs_dpoint(start, end, "numeric") for start, end in key_paths_1]
    robot_1_paths = stringify_paths(robot_1_buttons)

    robot_2_buttons = [
        [
            bfs_dpoint(start, end, "arrow")
            for start, end in zip("A" + robot_1_path, robot_1_path)
        ]
        for robot_1_path in robot_1_paths
    ]
    robot_2_paths = [stringify_paths(buttons) for buttons in robot_2_buttons]
    # flatten and remove duplicates
    robot_2_paths_simple = flatten_remove_dupes(robot_2_paths)

    # breakpoint()

    my_buttons = [
        [
            bfs_dpoint(start, end, "arrow")
            for start, end in zip("A" + robot_2_path, robot_2_path)
        ]
        for robot_2_path in robot_2_paths_simple
    ]
    my_paths = [stringify_paths(buttons) for buttons in my_buttons]
    my_paths_simple = flatten_remove_dupes(my_paths)

    return (robot_1_paths, robot_2_paths_simple, my_paths_simple)


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    numeric_targets = read_data(filename)

    rich.print(numeric_targets)
    for code in numeric_targets:
        console.print(Rule(f"{code}"), width=30)
        # rich.print(code)
        robot_1 = bfs_process_doorcode(code)
        rich.print(robot_1)
        # breakpoint()

    #     print(f"{me=}")
    #     print(f"{len(me)=}")
    #     print(f"{robot_2=}")
    #     print(f"{robot_1=}")
    # breakpoint()


rich.print(f"""test data: {part1(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    # rich.print(f"""test data: {part2(FNAME_TEST)}""")
    rich.print(f"""Problem input: {part2(fname)}""")


# Target 379A

# robot_1
["^A", "^^<<A", ">>A", "vvvA", ""]  # 3  # 7  # 9  # A

# robot_2
[
    # 3
    "<A",  # ^
    ">A",  # A
    # 7 path from 3-7 is different
    "<A",  # ^
    "A",  # ^
    "v<A",  # <
    "A",  # <
    ">>^A",  # A
    # 9
    "vA",  # >
    "A",  # >
    "^A",  # A
    # A
    "<vA",  # v
    "A",  # v
    "A",  # v
    ">^A",  # A
    "",
]

# me
[
    # 3
    "v<<A",  # <
    ">>^A",  # A
    "vA",  # >
    "^A",  # A
    # 7
    # different from test
    "v<<A",  # <
    ">>^A",  # A
    "A",  # A
    "<vA",  # v
    "<A",  # <
    # Same
    ">>^A",  # A
    "A",  # A
    "vA",  # >
    # Different
    "A",  # >
    "<^A",  # ^
    ">A",  # A
    # Same
    "<vA",  # v
    ">^A",  # A
    "A",  # A
    "<A",  # ^
    ">A",  # A
    "v<<A",  # <
    ">A",  # v
    ">^A",  # A
    "A",  # A
    "A",  # A
    "vA",  # >
    "<^A",  # ^
    ">A",  # A
    "",
]

test_solution = [
    # 3
    "<v<A",  # <
    ">>^A",  # A
    "vA",  # >
    "^A",  # A
    # 7 path from 3-7 is diffferent
    "<vA",  # v
    "<A",  # <
    "A",  # <
    # Same
    ">>^A",  # A
    "A",  # A
    "vA",  # >
    # Different
    "<^A",  # ^
    ">A",  # A
    "A",  # A
    "vA",  # >
    "^A",  # A
    # Same
    "<vA",  # v
    ">^A",  # A
    "A",  # A
    "<A",  # ^
    ">A",  # A
    "<v<A",  # <
    ">A",  # v
    ">^A",  # A
    "A",  # A
    "A",  # A
    "vA",  # >
    "<^A",  # ^
    ">A",  # A
    "",
]


ts_robot_2 = [
    # 3
    "<A",  # ^
    ">A",  # A
    # 7 path from 3-7 is different
    "v<<A",  # <
    "A",  # <
    ">^A",  # ^
    "A",  # ^
    ">A",  # A
    # 9
    "vA",  # >
    "A",  # >
    "^A",  # A
    # A
    "<vA",  # v
    "A",  # v
    "A",  # v
    ">^A",  # A
]

ts_robot_1 = [
    "^A",  # 3
    "<<^^A",  # 7
    ">>A",  # 9
    "vvvA",  # A
]
