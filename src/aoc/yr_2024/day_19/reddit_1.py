#!/usr/bin/env python

from pathlib import Path

import rich
from rich.rule import Rule

dname = Path("../../../../resources/2024/")
fname = dname / "d19.txt"
FNAME_TEST = "test_data.txt"


def find_syl(design, syll_tot, res=0, cache=None):
    """recursive function"""
    # rich.print(f"{design=}, {res=}")
    # rich.print(syll_tot)
    # rich.print(cache)
    # breakpoint()

    if cache is None:
        cache = {}
    if design in cache:
        return cache[design]
    if len(design) == 0:
        return cache.setdefault(design, 1)
    # reduce number of syllables to check
    syll = [elem for elem in syll_tot if elem in design]
    if len(syll) == 0:  # none found
        return cache.setdefault(design, 0)
    # All the syllables that can start `design`
    start = [elem for elem in syll if design.startswith(elem)]
    if len(start) == 0:
        return cache.setdefault(design, 0)
    for prefix in start:
        # Recurse, design gets smaller, syll is a potentially smaller set
        res += find_syl(design.removeprefix(prefix), syll, cache=cache)
    return cache.setdefault(design, res)


def part_2(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]

    count1, count2 = 0, 0
    syll_tot = list(map(str.strip, lines[0].split(",")))

    # Start a new cache for each file.
    cache = {}
    for i, design in enumerate(lines[2:]):
        res = find_syl(design, syll_tot, res=0, cache=cache)
        # breakpoint()

        if res > 0:
            count1 += 1
        count2 += res

    rich.print(f"part1: {count1}")
    rich.print(f"part2: {count2}")
    return count1, count2


part_2(FNAME_TEST)
rich.print(Rule())
part_2(fname)
