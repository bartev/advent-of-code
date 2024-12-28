"""Tests for AOC Day 21"""

import json

import aoc.yr_2024.day_21.puzzle as p
import pytest


# def test_part1():
#     assert 1 == 1


# def test_part2():
#     assert 1 == 1


def test_filter_shortest_paths():
    buttons_1 = [["<"], ["^"], ["^^>", "^>^", ">^^"], ["vvv"]]
    buttons_2 = [
        ["<"],
        ["^", "A", "BB"],
        ["^^>", "^>^", ">^^", "CCC", "ccc", "CDCD"],
        ["vvv"],
    ]

    buttons_2_expected = [
        ["<"],
        ["^", "A"],
        ["^^>", "^>^", ">^^", "CCC", "cccd"],
        ["vvv"],
    ]
    assert buttons_1 == p.filter_shortest_paths(buttons_1)
    assert buttons_2_expected == p.filter_shortest_paths(buttons_2)


test_filter_shortest_paths()
