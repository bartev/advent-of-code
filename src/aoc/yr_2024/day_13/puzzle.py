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

import rich
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
rprint(Panel.fit("[bold green]Part 1"))

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


def find_all_move_combos_faster(machine: Machine) -> int:
    """Loop over 1 variable, check if remainder is a multiple
    Go along A first, and stop at first value.
    Fewer A and more B will be less expensive
    """
    A, B, D = machine
    a_max = max(D.row // A.row, D.col // A.col) + 1
    # b_max = min(D.row // B.row, D.col // B.col) + 1

    results = None
    for a in range(a_max):
        remainder = D - A * a
        if remainder.col < 0 or remainder.row < 0:
            break

        if remainder.row % B.row == 0 and remainder.col % B.col == 0:
            b1 = remainder.row // B.row
            b2 = remainder.col // B.col
            if b1 == b2:
                results = (a, b1)
                break
    return [results]


def find_machine_costs_faster(machine: Machine) -> int:
    """Loop over 1 variable, check if remainder is a multiple
    Go along A first, and stop at first value.
    Fewer A and more B will be less expensive
    """
    A, B, D = machine
    a_max = max(D.row // A.row, D.col // A.col) + 1
    # b_max = min(D.row // B.row, D.col // B.col) + 1

    results = 0
    for a in range(a_max):
        remainder = D - A * a
        if remainder.col < 0 or remainder.row < 0:
            break

        if remainder.row % B.row == 0 and remainder.col % B.col == 0:
            b1 = remainder.row // B.row
            b2 = remainder.col // B.col
            if b1 == b2:
                results = cost_per_combo((a, b1))
                break
    return results


def cost_per_combo(move: Move) -> int:
    """a costs 3, b costs 1"""
    a, b = move
    return 3 * a + b


def cheapest_move_cost(machine) -> int:
    """Cost of the cheapest move for a machine (or None)"""
    moves = find_all_move_combos(machine)
    # moves = find_all_move_combos_faster(machine)
    costs = [cost_per_combo(move) for move in moves if move]
    return min(costs) if costs else None


def solve_n_m(machine: Machine) -> Moves:
    """Get all (n, m) moves for A & B
    Current solution IGNORES DEGENERATE CASES (colinear)
    Assumes a single solution.

    Use algebra
    nA + mB = D (2 eqn)
    solve for m(n, Ax, Bx, Dx)
    substitute to get n(Ax, Ay, Bx, By, Dx, Dy)

         (Dx - n * Ax)
    m = -------------
              Bx

         (Dx * By - Dy * Bx)
    n = --------------------
         (Ax * By - Ay * Bx)

    Find all n, m that are integers

    Check 3 cases:
    * get angle alpha = angle between D and A
    * get angle beta = angle between D and B

    1. If alpha == 0 => A and D are colinear
      a. Check for D = nA
    2. If beta == 0 => B and D are colinear
      a. Check for D = mB
    3. If alpha and beta == 0, find optimal n, m
      a. Consider if |A| > 3 |B|
      b. Could have a large number of solutions if brute force it
      c. A could be a multiple of B (or vice versa)
    4. A + B is colinear with D
    5. If sign(alpha) == sign(beta) => not solvable
    6. Use equations above to solve for n, m
    """
    # Not using n, m so as not to interfere with my debugger commands

    A, B, D = machine
    ax, ay = A.row, A.col
    bx, by = B.row, B.col
    dx, dy = D.row, D.col
    n_numer = dx * by - dy * bx
    n_denom = ax * by - ay * bx

    # if the n_multiplier is an int, look at m_mult
    if n_numer % n_denom == 0:
        n_mult = n_numer // n_denom
        m_numer = dx - n_mult * ax
        m_denom = bx
        if m_numer % m_denom == 0:
            m_mult = m_numer // m_denom
            res = (n_mult, m_mult)
        else:
            res = None
    else:
        res = None
    return res


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

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


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
    modified_d_machines = [modify_d(machine) for machine in machines]
    machine_moves = [solve_n_m(machine) for machine in modified_d_machines]
    costs = [cost_per_combo(move) for move in machine_moves if move]
    return sum(costs)


rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
