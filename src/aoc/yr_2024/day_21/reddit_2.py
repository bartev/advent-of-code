#!/usr/bin/env python

# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2024/21.py

import heapq
import re
from pathlib import Path

import rich
from rich.rule import Rule

dname = Path("../../../../resources/2024/")
fname = dname / "d21.txt"


def ints(s):
    """Return a list of all ints in s
    Example:
    > ints('xy2b-34y5-6z')
    [2, -34, 5, -6]
    """
    return [int(x) for x in re.findall(r"-?\d+", s)]


infile = "test_data.txt"
D = open(infile).read().strip()
DD = open(fname).read().strip()

pad1 = ["789", "456", "123", " 0A"]
pad2 = [" ^A", "<v>"]


def get_pad1(p1):
    r, c = p1
    if not (0 <= r < len(pad1) and 0 <= c < len(pad1[r])):
        return None
    if pad1[r][c] == " ":
        return None
    return pad1[r][c]


def get_pad2(p1):
    r, c = p1
    # print(f"get_pad2 {r=}, {c=}")
    if not (0 <= r < len(pad2) and 0 <= c < len(pad2[r])):
        return None
    if pad2[r][c] == " ":
        return None
    return pad2[r][c]


def apply_pad1(p, move):
    if move == "A":
        return (p, get_pad1(p))
    if move == "<":
        return ((p[0], p[1] - 1), None)
    if move == "^":
        return ((p[0] - 1, p[1]), None)
    if move == ">":
        return ((p[0], p[1] + 1), None)
    if move == "v":
        return ((p[0] + 1, p[1]), None)


def apply_pad2(p, move):
    if move == "A":
        return (p, get_pad2(p))
    if move == "<":
        return ((p[0], p[1] - 1), None)
    if move == "^":
        return ((p[0] - 1, p[1]), None)
    if move == ">":
        return ((p[0], p[1] + 1), None)
    if move == "v":
        return ((p[0] + 1, p[1]), None)


def solve1(code, pads):
    # cost_move, p1, move, out, path
    # breakpoint()

    start = [0, (3, 2), "A", "", ""]
    Q = []
    heapq.heappush(Q, start)
    SEEN = {}
    while Q:
        d, p1, p2, out, path = heapq.heappop(Q)
        assert p2 in "<>v^A"
        if out == code:
            return d
        if not code.startswith(out):
            continue
        if get_pad1(p1) is None:
            continue
        key = (p1, p2, out)
        if key in SEEN:
            assert d >= SEEN[key], f"{key=} {d=} {SEEN[key]=}"
            continue

        for move in "^<v>A":
            # breakpoint()

            new_p1 = p1
            new_out = out
            new_p1, output = apply_pad1(p1, move)
            if output is not None:
                new_out = out + output
            cost_move = cost2(move, p2, pads)
            new_path = path  # + cost_move
            assert cost_move >= 0
            heapq.heappush(Q, [d + cost_move, new_p1, move, new_out, new_path])


DP = {}


def cost2(ch, prev_move, pads):
    breakpoint()

    key = (ch, prev_move, pads)
    if key in DP:
        return DP[key]
    if pads == 0:
        return 1
    else:
        assert ch in ["^", ">", "v", "<", "A"]
        assert prev_move in ["^", ">", "v", "<", "A"]
        assert pads >= 1
        # cost of pressing ch with [pads] pads all of which are on A
        Q = []
        start_pos = {"^": (0, 1), "<": (1, 0), "v": (1, 1), ">": (1, 2), "A": (0, 2)}[
            prev_move
        ]
        heapq.heappush(Q, [0, start_pos, "A", "", ""])
        SEEN = {}
        while Q:
            d, p, prev, out, path = heapq.heappop(Q)
            # print(d,p,prev,out,path)
            # assert d==len(path), f'{d=} {len(path)=} {path=}'
            if get_pad2(p) is None:
                continue
            if out == ch:
                # assert len(path) == d, f'{new_path=} {new_d=}'
                # slow_path = cost2_slow(ch, prev_move, pads)
                # assert len(path) == len(slow_path), f'{ch=} {prev_move=} {pads=} {len(path)=} {len(slow_path)=} {path=} {slow_path=}'
                # print(f'{key=} {DP[key]=}')
                DP[key] = d
                return d
            elif len(out) > 0:
                continue
            seen_key = (p, prev)
            if seen_key in SEEN:
                assert d >= SEEN[seen_key]
                continue
            SEEN[seen_key] = d
            for move in ["^", "<", "v", ">", "A"]:
                new_p, output = apply_pad2(p, move)
                cost_move = cost2(move, prev, pads - 1)
                new_d = d + cost_move  # len(cost_move)
                new_path = path  # + cost_move
                new_out = out
                if output is not None:
                    new_out = new_out + output
                heapq.heappush(Q, [new_d, new_p, move, new_out, new_path])
        assert False, f"{ch=} {pads=}"


rich.print(Rule("test file"))

p1 = 0
p2 = 0
for line in D.split("\n"):
    s1 = solve1(line, 2)
    s2 = solve1(line, 25)
    line_int = ints(line)[0]
    print(line, line_int, s1, s2)
    p1 += s1 * line_int
    p2 += s2 * line_int


print(f"{p1=}")
print(f"{p2=}")

rich.print(Rule("my puzzle file"))

p1 = 0
p2 = 0
for line in DD.split("\n"):
    s1 = solve1(line, 2)
    s2 = solve1(line, 25)
    line_int = ints(line)[0]
    print(line, line_int, s1, s2)
    p1 += s1 * line_int
    p2 += s2 * line_int


print(f"{p1=}")
print(f"{p2=}")
