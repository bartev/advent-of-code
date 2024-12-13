#!/usr/bin/env python

"""
Author: Bartev
Date: 2024-12-12

aA + bB = D

a * A1 + b * B1 = D1
a * A2 + b * B2 = D2

a, b must be positive integers

so
a <= D1 / A1
a <= D2 / A2

b <= D1 / B1
b <= D2 / B2

Use the Position class
It has scalar multiplication and addition of vectors

"""

import logging
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.position import Position
from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dname = Path("../../../../resources/2024/")
fname = dname / "d13.txt"
FNAME_TEST = "test_data.txt"


def parse_coord(line: str) -> Position:
    """Parse a line that looks like one of:
    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """
    X, y = line.split("X")[1][1:].split(",")
    Y = y.split("Y")[1][1:]
    return Position(int(X), int(Y))


def read_data(filename: str):
    """Read the data into groups of coordinates, A, B, D
    D is the destination.
    """

    def parse_group(group: list[str]) -> tuple[Position, Position, Position]:
        """Parse the 3 lines of input"""
        return [parse_coord(line) for line in group]

    all_groups = []
    with open(filename, "r", encoding="utf8") as f:
        group = []
        for line in f:
            line = line.strip()
            if line:
                group.append(line)
            else:
                all_groups.append(group)
                group = []
        all_groups.append(group)
    return [parse_group(group) for group in all_groups]


# ########## Part

rprint(Rule("Part ", style="bold green"))
rprint(Panel.fit("[bold green]Part "))

# A, B, D
Machine = tuple[Position, Position, Position]
Machines = list[Machine]
Move = tuple[int, int]
Moves = list[Move]


def find_all_move_combos(machine: Machine) -> Moves:
    """loop over possible values.
    Brute force.
    Limit how far to go.
    """
    A, B, D = machine
    # // rounds down
    a_max = min(D.row // A.row, D.col // A.col) + 1
    b_max = min(D.row // B.row, D.col // B.col) + 1

    valid_combos = []
    for a in range(a_max):
        for b in range(b_max):
            delta = A * a + B * b - D
            if delta.row > 0 or delta.col > 0:
                break
            if delta.row == 0 and delta.col == 0:
                valid_combos.append((a, b))
    return valid_combos


def cost_per_combo(move: Move) -> int:
    """a costs 3, b costs 1"""
    a, b = move
    return 3 * a + b


def cheapest_move_cost(machine) -> int:
    """Cost of the cheapest move for a machine (or None)"""
    moves = find_all_move_combos(machine)
    costs = [cost_per_combo(move) for move in moves if move]
    return min(costs) if costs else None


@time_it
def part1(filename: str) -> int:
    """Run part  given the input file
    Return value should be the solution"""
    machines = read_data(filename)
    # mach_combos = [find_all_move_combos(machine) for machine in machines]
    mach_costs = [cheapest_move_cost(machine) for machine in machines]

    # return len(mach_combos), len(mach_costs), len(machines)
    return sum(cost for cost in mach_costs if cost)


rprint(f"""test data: {part1(FNAME_TEST)}""")
rprint(f"""Problem input: {part1(fname)}""")

# ########## Part

rprint(Rule("Part ", style="bold red"))
rprint(Panel.fit("[bold red]Part "))


def modify_d(machine):
    """Add `10000000000000` to D x and y values"""
    value = 10000000000000
    d_add = Position(value, value)
    A, B, D = machine
    return A, B, D + d_add


@time_it
def part2(filename: str) -> int:
    """Run part  given the input file
    Return value should be the solution"""
    machines = read_data(filename)
    # mach_combos = [find_all_move_combos(machine) for machine in machines]
    modified_d_machines = [modify_d(machine) for machine in machines]
    mach_costs = [cheapest_move_cost(machine) for machine in modified_d_machines]

    # return len(mach_combos), len(mach_costs), len(machines)
    return sum(cost for cost in mach_costs if cost)


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
