"""Tests for AOC Day 14"""

import json
import re

import pytest

import aoc.yr_2024.day_14.puzzle as p
from aoc.pyutils.position import Position


def test_parse_line():
    """Parse the line to get the position and velocity"""
    line = "p=b0,4 v=3,-3"
    assert p.parse_line(line) == (Position(4, 0), Position(-3, 3))


def test_part1():
    assert 1 == 1


def test_part2():
    assert 1 == 1
