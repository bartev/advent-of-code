#!/usr/bin/env python

from pathlib import Path

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

console = Console()

dname = Path("../../../../resources/2024/")
fname = dname / "d04.txt"
FNAME_TEST = "test_data.txt"

# ########## Part 1

"""
ideas

The data is 140x140 char.

String search
1. Create strings L-R, T-B and NW-SE, NE-SW
2. Search for xmas or samx in all strings.

XMAS 360 search
1. Find indices of all X's
2. Search 360 for X-M-A-S
3. If x, y are the position of the index,
  a. if x < 4, don't go left or NW or SW
  b. if y < 4, don't go up or NW or NE
  c. if x > (cols - 4), don't go right or NE or SE
  d. if y > (rows - 4), don't go down or SW or SE

"""

rprint(Panel.fit("Part 1"))


def count_xmas(s: str) -> int:
    """Count occurences of `XMAS` in s (forward and backward)"""
    _s = s.upper()
    xmas = _s.count("XMAS")
    samx = _s.count("SAMX")
    return xmas + samx


def read_file(filename: str) -> str:
    """Read the file into a list of strings"""
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines


def create_diagonal_lines(lines: list[str]) -> list[str]:
    """Create diagonal strings from a list of strings"""
    width = len(lines[0])
    height = len(lines)
    sw_ne_diags = []
    nw_se_diags = []
    for y in range(height * 2):
        yy = y
        x = 0
        x_rev = width - 1
        line = []
        line_rev = []
        while x < width and yy >= 0:
            if yy < height:
                char = lines[yy][x]
                line.append(char)
                char_rev = lines[yy][x_rev]
                line_rev.append(char_rev[::-1])
            x = x + 1
            x_rev = x_rev - 1
            yy = yy - 1
        sw_ne_diags.append(line)
        nw_se_diags.append(line_rev)
    sn_diags = list(map("".join, sw_ne_diags))
    ns_diags = list(map("".join, nw_se_diags))
    return sn_diags, ns_diags


def transpose_lines(lines: list[str]) -> list[str]:
    """Transpose list of strings into vertical strings"""
    transposed = zip(*lines)
    return ["".join(col) for col in transposed]


def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    lines = read_file(filename)
    verts = transpose_lines(lines)
    diags_1, diags_2 = create_diagonal_lines(lines)

    cnt_1 = sum(map(count_xmas, lines))
    cnt_2 = sum(map(count_xmas, verts))
    cnt_3 = sum(map(count_xmas, diags_1))
    cnt_4 = sum(map(count_xmas, diags_2))
    return cnt_1 + cnt_2 + cnt_3 + cnt_4


console.print(f"""test data: {part1(FNAME_TEST)}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Panel.fit("Part 2"))


def find_all_indices(line: str, pat: str = "MAS"):
    """Find all the indices of the letter A in MAS or SAM in a line"""
    indices = []
    start = 0
    while True:
        index = line.find(pat, start)
        if index == -1:
            break
        indices.append(index)
        start = index + 1
    return indices


def flatten_and_sort(nested: list) -> list[tuple]:
    """Flatten and sort a nested list of tuples"""
    flat = [tup for sublist in nested for tup in sublist]
    return sorted(flat, key=lambda x: (x[0], x[1]))


def find_matches(tups1, tups2) -> list[tuple]:
    """find tuples that are in both tups1 and tups2"""
    return [tup for tup in tups1 if tup in tups2]


def diag_match(lines: list[str], idx: tuple) -> bool:
    """True if spells MAS in any diag dir"""
    y, x = idx
    nw = lines[y - 1][x - 1]
    ne = lines[y - 1][x + 1]

    sw = lines[y + 1][x - 1]
    se = lines[y + 1][x + 1]

    matches = ["MS", "SM"]
    # breakpoint()

    return (nw + se in matches) and (ne + sw in matches)


def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    lines = read_file(filename)
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    indices = []
    for y, line in enumerate(lines):
        _indices_a = find_all_indices(line, "A")
        indices_a = [(y, x) for x in _indices_a if x != -1]
        indices.append(indices_a)
    indices = flatten_and_sort(indices)
    # `A` can't be on the edges
    indices = [(y, x) for y, x in indices if 0 < y < max_y and 0 < x < max_x]
    results = map(lambda x: diag_match(lines, x), indices)
    return sum(results)


rprint(f"""test data: {part2(FNAME_TEST)}""")

rprint(f"""Problem input: {part2(fname)}""")
