#!/usr/bin/env python

import re
from pathlib import Path

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

console = Console()

dname = Path("../../../../resources/2024/")
fname = dname / "d03.txt"
fname_test = "test_data.txt"

# ########## Part 1

rprint(Panel.fit("Part 1"))


def read_file(filename: str) -> str:
    with open(filename, "r") as f:
        content = f.read()
    return content


def eval_match(to_eval: str) -> int:
    """Convert mul(3,4) to 3 x 4 and eval"""
    pat = r"mul\((\d*),(\d*)\)"
    match = re.search(pat, to_eval)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        return a * b
    return None


def find_matches_in_str(s: str) -> list[str]:
    pat = r"mul\(\d*,\d*\)"
    return re.findall(pat, s)


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    s = read_file(filename)
    matches = find_matches_in_str(s)
    return sum([eval_match(m) for m in matches])


console.print(f"""test data: {part1(fname_test)}""")

rprint(f"""Problem input: {part1(fname)}""")

# # ########## Part 2

rprint(Panel.fit("Part 2"))


def truncate_dont(s: str) -> str:
    """Truncate everything after `don't()`"""
    idx = s.find("don't()")
    res = s if idx == -1 else s[:idx]
    return res


def flatten_list(nested: list) -> list:
    """Flatten a list of lists"""
    return [item for sublist in nested for item in sublist]


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    s = read_file(filename)
    substrings = s.split("do()")
    strings_to_eval = [truncate_dont(subs) for subs in substrings]
    list_matches = [find_matches_in_str(ste) for ste in strings_to_eval]
    matches = flatten_list(list_matches)
    # print(list_matches)
    # print(matches)
    return sum([eval_match(m) for m in matches])


rprint(f"""test data: {part2("test_data_2.txt")}""")

rprint(f"""Problem input: {part2(fname)}""")
