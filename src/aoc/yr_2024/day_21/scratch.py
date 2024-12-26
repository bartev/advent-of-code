#!/usr/bin/env python

from collections import deque
from functools import cache
from itertools import product

import rich


def read_data(filename: str) -> list[str]:
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        content = [line.strip() for line in f.readlines()]
    return content


# ########## Part 1

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


# Pass the keyboard name, not the dict, since we a dict is not
# hashable and can't be used with caching
@cache
def bfs_shortest_paths(start_str: str, end_str: str, keypad_name: str) -> list[str]:
    """Find all the shortest paths between 2 points on a grid, avoiding the gap"""
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    # reverse_directions = {v: k for k, v in directions.items()}

    keypad = numeric_keypad if keypad_name == "numeric" else arrow_keypad
    start = keypad[start_str]
    end = keypad[end_str]
    queue = deque([(start, "")])
    visited = {}
    shortest_paths = []
    min_length = float("inf")
    keypad_bounds = set(keypad.values())

    while queue:
        current, path = queue.popleft()

        if len(path) > min_length:  # Stop if longer than the shortest found
            continue

        if current == end:
            if len(path) < min_length:
                min_length = len(path)
                shortest_paths = [path]
            elif len(path) == min_length:
                shortest_paths.append(path)
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

    return shortest_paths


def stringify_paths(path_list: list[str]):
    """Join a list of paths with A into a single string"""
    return ["A".join(path) + "A" for path in product(*path_list)]


def keep_min_len_strings(strings: list[str]) -> list[str]:
    """Keep all strings that are the shortest length"""
    min_length = min(len(s) for s in strings)
    return [s for s in strings if len(s) == min_length]


def flatten_remove_dupes(nested_list: list[list]) -> list:
    """Flatten 1 level of a nested list"""
    return list({item for sublist in nested_list for item in sublist})


def bfs_process_doorcode(code: str):
    """Process a single doorcode with BFS"""
    # Get all paths for robot 1
    key_paths_1 = zip("A" + code, code)
    robot_1_buttons = [
        bfs_shortest_paths(start, end, "numeric") for start, end in key_paths_1
    ]
    robot_1_paths = keep_min_len_strings(stringify_paths(robot_1_buttons))

    robot_2_buttons = [
        [
            bfs_shortest_paths(start, end, "arrow")
            for start, end in zip("A" + robot_1_path, robot_1_path)
        ]
        for robot_1_path in robot_1_paths
    ]
    robot_2_paths = [stringify_paths(buttons) for buttons in robot_2_buttons]
    # flatten and remove duplicates
    robot_2_paths_simple = keep_min_len_strings(flatten_remove_dupes(robot_2_paths))

    # breakpoint()

    my_buttons = [
        [
            bfs_shortest_paths(start, end, "arrow")
            for start, end in zip("A" + robot_2_path, robot_2_path)
        ]
        for robot_2_path in robot_2_paths_simple
    ]
    my_paths = [stringify_paths(buttons) for buttons in my_buttons]
    my_paths_simple = keep_min_len_strings(flatten_remove_dupes(my_paths))

    # return robot_1_paths, robot_2_paths_simple, my_paths_simple
    return my_paths_simple


def complexity(code: str) -> int:
    """Get the complexity for a code"""
    paths = bfs_process_doorcode(code)
    numeric_part = int(code.rstrip("A"))
    return numeric_part * len(paths[0])


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    numeric_targets = read_data(filename)

    rich.print(numeric_targets)
    res = sum(complexity(code) for code in numeric_targets)

    return res


rich.print(f"""test data: {part1("test_data.txt")}""")

# ########## Part 2


def proc_doorcode_1(prev_robot_paths: list[str]) -> list[str]:
    """Take the output of a robot, and let another robot (or me) work on it"""

    next_robot_buttons = [
        [
            bfs_shortest_paths(start, end, "arrow")
            for start, end in zip("A" + prev_robot_path, prev_robot_path)
        ]
        for prev_robot_path in prev_robot_paths
    ]
    next_robot_paths = [stringify_paths(buttons) for buttons in next_robot_buttons]
    # Flatten the list
    next_robot_paths_flattened = flatten_remove_dupes(next_robot_paths)
    # only keep the shortest paths
    return keep_min_len_strings(next_robot_paths_flattened)


def bfs_process_doorcode_multiple(code: str, num_robots: int = 2) -> list[str]:
    """Process a single doorcode with BFS for num_robots + me"""
    # Get all paths for robot 1
    key_paths_1 = zip("A" + code, code)
    # breakpoint()

    robot_1_buttons = [
        bfs_shortest_paths(start, end, "numeric") for start, end in key_paths_1
    ]
    robot_1_paths = keep_min_len_strings(stringify_paths(robot_1_buttons))

    prev_robot_paths = robot_1_paths
    for _ in range(num_robots):
        next_robot_paths = proc_doorcode_1(prev_robot_paths)
        prev_robot_paths = next_robot_paths.copy()

    # return robot_1_paths, robot_2_paths_simple, my_paths_simple
    return next_robot_paths


def complexity_2(code: str, path_len: int) -> int:
    """Get the complexity for a code"""
    numeric_part = int(code.rstrip("A"))
    return numeric_part * path_len


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    numeric_targets = read_data(filename)

    rich.print(numeric_targets)
    my_codes = [
        (code, len(bfs_process_doorcode_multiple(code)[0])) for code in numeric_targets
    ]

    # res = sum(complexity(code) for code in numeric_targets)
    breakpoint()

    return my_codes


# rich.print(f"""test data: {part2("test_data.txt")}""")
