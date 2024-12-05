#!/usr/bin/env python

"""
Advent of code day 5
Author: Bartev
Date: 2024-12-04
"""

from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

dname = Path("../../../../resources/2024/")
fname = dname / "d05.txt"
FNAME_TEST = "test_data.txt"

# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = f.read()

    part1, part2 = content.strip().split("\n\n")

    # parse rules into list of tuples
    rules = [tuple(map(int, line.split("|"))) for line in part1.splitlines()]

    list_pages = [list(map(int, line.split(","))) for line in part2.splitlines()]
    return rules, list_pages


def relevant_rules(rules: list[tuple], pages: list[int]) -> list[tuple]:
    """return the list of rules that apply to the current pages"""
    return [rule for rule in rules if rule[0] in pages and rule[1] in pages]


def rule_passes(rule: tuple, pages: list[int]) -> bool:
    """true if the page order passes the rule"""
    before = rule[0]
    after = rule[1]
    return pages.index(before) < pages.index(after)


def apply_rules(rules: list[tuple], pages: list[int]) -> bool:
    """True if all the rules pass"""

    # rprint(f"{type(pages)=}")
    rel_rules = relevant_rules(rules, pages)
    # rprint(f"{len(rel_rules)=}")
    pass_fail = [rule_passes(rule, pages) for rule in rel_rules]
    return all(pass_fail)


def middle_page(pages: list[int]) -> int:
    return pages[(len(pages) - 1) // 2]


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    rules, list_pages = read_data(filename)
    # rel_rules = relevant_rules(rules, list_pages[0])
    # rprint(f"num rel rules = {len(rel_rules)}")
    # rprint(f"num rules = {len(rules)}")
    res = [middle_page(pages) for pages in list_pages if apply_rules(rules, pages)]
    # res = apply_rules(rules, list_pages[0])
    # rprint(res)
    return sum(res)


rprint(f"""test data: {part1(FNAME_TEST)}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    pass


rprint(f"""test data: {part2(FNAME_TEST)}""")

rprint(f"""Problem input: {part2(fname)}""")
