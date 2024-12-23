#!/usr/bin/env python

import heapq
import logging
import math
from collections import deque
from itertools import combinations_with_replacement
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
fname = dname / "d19.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        towels = [towel.strip() for towel in f.readline().strip().split(",")]
        patterns = [line.strip() for line in f if line.strip()]
    return towels, patterns


# read_data(FNAME_TEST)

# ########## Part 1

rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


def find_towel_combos(design, towels):
    """Find all towel combinations that can create design"""

    def helper(current_design, path):
        """The recursive function helper"""
        # base case: if current_design is empty, we have found a path
        if not current_design:
            return [path]

        valid_towels = [towel for towel in towels if current_design.startswith(towel)]

        # Recursively check each towel
        combinations = []
        for towel in valid_towels:
            remaining_design = current_design.removeprefix(towel)
            combinations.extend(helper(remaining_design, path + [towel]))
        return combinations

    # Start the call with the whole design and an empty list
    return helper(design, [])


def count_all_towel_combos(towels: list[str]) -> dict:
    """Count how many ways you can make each towel design from smaller designs
    Return a dict of towel: count"""
    reduced_towels, redundant_towels = reduce_redundancies_towels(towels)
    # there's only 1 way to get reduced_towels
    counts_dict = {towel: 1 for towel in reduced_towels}
    for towel in redundant_towels:
        combos = find_towel_combos(towel, towels)
        counts_dict[towel] = len(combos)
    return counts_dict


def can_be_formed(design, towels):
    """True if design can be formed with towels"""
    # breakpoint()

    if not design:
        return True

    for towel in towels:
        remainder = design.removeprefix(towel)
        if remainder != design:  # means towel was successfully returned
            if can_be_formed(remainder, towels):
                return True
    return False


# design = "brwrr"
# towels = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]


# def foo(design, towels):
#     print(f"{design=}, {towels=}")
#     res = map("".join, combinations_with_replacement(towels + [""], len(design)))
#     # rich.print([x for x in res if len(x) == len(design)])
#     rich.print(sorted([x for x in res if x.startswith("b")]))
#     # return [x for x in res if x == design]


# rich.print(sorted(map("".join, combinations_with_replacement(["b", "r", "wr", ""], 5))))
# rich.print(sorted(combinations_with_replacement(["b", "r", "wr", ""], 5)))

# rich.print(foo(design, towels))


def reduce_redundancies_towels(towels):
    """Reduce the number of keys in towels.
    e.g., if I have b, bb, and bbb, I can replace all of these by b."""
    # Sort towels by length to get smallest units
    sorted_towels = sorted(towels, key=lambda x: (len(x), x))
    # store strings that cannot be formed by combinations of other strings
    reduced_towels = []
    redundant_towels = []
    # breakpoint()
    for towel in sorted_towels:
        # Check if towel can be formed from shorter towels
        if not can_be_formed(towel, reduced_towels):
            reduced_towels.append(towel)
        else:
            redundant_towels.append(towel)
    return reduced_towels, redundant_towels


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    towels, designs = read_data(filename)
    # Reduce complexity by removing towels that can be formed from smaller ones
    reduced_towels, _ = reduce_redundancies_towels(towels)
    rich.print(f"{len(towels)=}, {len(reduced_towels)=}")
    # can_form_design is a list of bools, true if it can be formed
    can_form_design = [can_be_formed(design, reduced_towels) for design in designs]
    return sum(can_form_design)


rich.print(f"""test data: {part1(FNAME_TEST)}""")
print()
rich.print(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


def find_shortest_towel_combo(design, towels):
    """Start with the longest strings, and stop looking when a solution is found"""

    def helper(current_design, path):
        """The recursive function helper"""
        # Base case: if current_design is empty, we found a path
        if not current_design:
            return [path]
        # Reduce the number further
        possible_towels = [towel for towel in towels if towel in current_design]
        # Sort longest to shortest, then alphabetically
        sorted_towels = sorted(possible_towels, key=lambda x: (-len(x), x))
        # Recursively check each towel
        combinations = []
        for towel in sorted_towels:
            remaining_design = current_design.removeprefix(towel)
            combinations.extend(helper(remaining_design, path + [towel]))
        return combinations

    # Start the call with the whole design and an empty list
    return helper(design, [])


def shortest_permutation_with_replacement(design, towels):
    """Find shortest permutation of towels to create design"""
    queue = deque([("", [])])
    sorted_towels = sorted(towels, key=lambda x: (-len(x), x))
    breakpoint()

    while queue:
        current, sequence = queue.popleft()
        rich.print(current, sequence)

        # if the current string matches the design, return the sequence
        if current == design:
            return sequence

        # if the current string is longer than the design, skip it
        if len(current) > len(design):
            continue

        # Add next candidate by appending each towel to the current string
        # Start with longest towels
        reduced_towels = [
            towel for towel in sorted_towels if towel.startswith(current[0])
        ]
        for towel in reduced_towels:
            new_string = current + towel
            if design.startswith(new_string):
                queue.append((new_string, sequence + [towel]))
            rich.print(queue)
            breakpoint()

    # if now solution is found
    return None


def shortest_permutation_dijkstra(design, towels):
    """Find the shortest permutation of towel that create design using
    Dijkstra's algorithm
    """
    # priority queue: (cost, current_string, sequence_of_towels_used)
    queue = [(0, "", [])]
    visited = set()

    while queue:
        cost, current, sequence = heapq.heappop(queue)

        # Stopping condition:
        # If the current string matches the design, return the sequence
        if current == design:
            return sequence

        # Skip if visited (we're looking for the shortest path)
        if current in visited:
            continue
        visited.add(current)

        # Add next towels by appending each towel to the current string
        for towel in towels:
            new_string = current + towel
            if design.startswith(new_string):
                heapq.heappush(queue, (cost + 1, new_string, sequence + [towel]))

    # If no solution found
    return None


def all_shortest_permutations_dijkstra(design, towels):
    """Find ALL the shortest permutations of towels that create design using
    Dijkstra's algorithm
    """

    # priority queue: (cost, current_string, sequence_of_towels_used)
    queue = [(0, "", [])]
    visited = {}
    shortest_length = float("inf")
    results = []

    while queue:
        cost, current, sequence = heapq.heappop(queue)
        print(f"{cost=}, {current=}, {sequence=}")
        breakpoint()

        # Skip if we already found shorter sequences for this string
        if current in visited and visited[current] < cost:
            continue
        visited[current] = cost

        # Stopping condition:
        # If the current string matches the design, return the sequence
        print(f"{current=}, {design=}")
        breakpoint()

        if current == design:
            if cost < shortest_length:
                shortest_length = cost
                results = [sequence]
            elif cost == shortest_length:
                results.append(sequence)
            print(f"{shortest_length=}, {results=}")
            continue

        # Add next towels by appending each towel to the current string
        for towel in towels:
            new_string = current + towel
            if design.startswith(new_string):
                heapq.heappush(queue, (cost + 1, new_string, sequence + [towel]))

    # If no solution found
    return results


def find_all_permutations(design, towels):
    """Find all distinct permutations (can blow up for large len(towels))"""
    # Queue: (current_string, sequence_of_towels_used)
    queue = deque([("", [])])
    results = []

    while queue:
        current, sequence = queue.popleft()

        # Stopping condition: if the current string matches the design
        if current == design:
            results.append(sequence)
            continue

        # Add next towels to extend the path
        for towel in towels:
            new_string = current + towel
            if design.startswith(new_string):  # Only explore valid prefixes
                queue.append((new_string, sequence + [towel]))

    return results


# ##### Reddit solution
# https://www.reddit.com/r/adventofcode/comments/1hhlb8g/comment/m3620el/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
cache = {}


def reddit_find_syllable(line, syll_tot, res=0):
    """Recurseive solution"""
    if line in cache:
        return cache[line]


# ##### End Reddit solution


def testing(design, towels, towel_combo_counts):
    """Found a bug when looking at the test data.
    Found 2 shortest paths
    [['r', 'rb', 'g', 'br'], ['r', 'rb', 'gb', 'r']]

    But, [g, br] and [gb, r] share a common permutation.

    [g, br], [g, b, r]
    [gb, r], [g, b, r]

    So instead of 2 ways to get 'gbr', or 4, there are actually 3.
    """
    rich.print(Rule())
    rich.print("design:", design)
    rich.print("towels:", towels)
    rich.print("towel_combo_counts:", towel_combo_counts)
    # perm = shortest_permutation_dijkstra(design, towels)
    perm = all_shortest_permutations_dijkstra(design, towels)
    rich.print("perm:", perm)
    # counts = [(towel, towel_combo_counts[towel]) for towel in perm]
    # rich.print("counts", counts)


def testing_all(design, towels, towel_combo_counts):
    """Found a bug when looking at the test data."""
    rich.print(Rule())
    rich.print("design:", design)
    rich.print("towels:", towels)
    rich.print("towel_combo_counts:", towel_combo_counts)
    perm = find_all_permutations(design, towels)
    rich.print("perm:", perm)
    # counts = [(towel, towel_combo_counts[towel]) for towel in perm]
    # rich.print("counts", counts)


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    towels, designs = read_data(filename)
    # Reduce complexity by removing towels that can be formed from smaller ones
    reduced_towels, redundant_towels = reduce_redundancies_towels(towels)
    towel_combo_counts = count_all_towel_combos(towels)
    print(f"{len(towels)=}, {len(reduced_towels)=}, {len(redundant_towels)=}")
    valid_designs = [
        design for design in designs if can_be_formed(design, reduced_towels)
    ]

    # testing("gbbr", towels, towel_combo_counts)
    # testing("rrbgbr", towels, towel_combo_counts)

    testing_all("gbbr", towels, towel_combo_counts)
    testing_all("rrbgbr", towels, towel_combo_counts)
    # count_ways_to_get_designs = [
    #     [
    #         towel_combo_counts[towel]
    #         for towel in shortest_permutation_dijkstra(design, towels)
    #     ]
    #     for design in valid_designs
    # ]
    # res = sum(map(math.prod, count_ways_to_get_designs))

    # ways_to_get_keys = [towel_combo_counts[towel] for towel in res]
    # return list(zip(valid_designs, count_ways_to_get_designs))


rich.print(f"""test data: {part2(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part2(fname)}""")
