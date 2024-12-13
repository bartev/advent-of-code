"""Tests for AOC Day 02"""

import json

import puzzle as p
import pytest

from aoc.pyutils.position import Position


# def test_part2():
#     assert 1 == 1


def test_parse_coord():
    line1 = "Button A: X+69, Y+23"
    line2 = "Button B: X+27, Y+71"
    line3 = "Prize: X=18641, Y=10279"

    assert Position(69, 23) == p.parse_coord(line1)
    assert Position(27, 71) == p.parse_coord(line2)
    assert Position(18641, 10279) == p.parse_coord(line3)


def test_read_data():
    expected = [
        [
            Position(row=94, col=34),
            Position(row=22, col=67),
            Position(row=8400, col=5400),
        ],
        [
            Position(row=26, col=66),
            Position(row=67, col=21),
            Position(row=12748, col=12176),
        ],
        [
            Position(row=17, col=86),
            Position(row=84, col=37),
            Position(row=7870, col=6450),
        ],
    ]
    assert p.read_data("test_data.txt") == expected


def test_part1():
    expected = 480
    fname = "test_data.txt"
    assert expected == p.part1(fname)
