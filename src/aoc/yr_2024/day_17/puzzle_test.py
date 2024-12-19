"""Tests for AOC Day 17

Writing tests

pytest.raises:
Used to check if a ValidationError is raised for invalid inputs.

Parameterized Tests:
The @pytest.mark.parametrize decorator is used to test multiple
invalid input scenarios in a single function, reducing duplication.


"""

import json

# import puzzle as p
import pytest
from aoc.yr_2024.day_17.puzzle import OpComputer
from pydantic import ValidationError


# Test valid program input
def test_valid_program():
    computer = OpComputer(program=[0, 1, 2, 7], a=5, b=10, c=15)
    assert computer.program == [0, 1, 2, 7]
    assert computer.a == 5
    assert computer.b == 10
    assert computer.c == 15


# Test program with invalid values (out of range)
# pytest.raises:
# Used to check if a ValidationError is raised for invalid inputs.


def test_invalid_program_value():
    with pytest.raises(ValidationError, match="must satisfy 0 <= n < 8"):
        OpComputer(program=[0, 8, 3], a=1, b=2, c=3)


# Test empty program list
def test_empty_program():
    computer = OpComputer(program=[], a=0, b=0, c=0)
    assert computer.program == []
    assert computer.a == 0
    assert computer.b == 0
    assert computer.c == 0


# Test invalid types for fields
# Parameterized Tests:

# The @pytest.mark.parametrize decorator is used to test
# multiple invalid input scenarios in a single function,
# reducing duplication.


@pytest.mark.parametrize(
    "program, a, b, c",
    [
        ("not_a_list", 1, 2, 3),  # Invalid program type
        ([0, 1, 2], "not_an_int", 2, 3),  # Invalid 'a' type
        ([0, 1, 2], 1, "not_an_int", 3),  # Invalid 'b' type
        ([0, 1, 2], 1, 2, "not_an_int"),  # Invalid 'c' type
    ],
)
def test_invalid_field_types(program, a, b, c):
    with pytest.raises(ValidationError):
        OpComputer(program=program, a=a, b=b, c=c)


# Test program with negative numbers
def test_negative_program_values():
    with pytest.raises(ValidationError, match="must satisfy 0 <= n < 8"):
        OpComputer(program=[-1, 2, 3], a=1, b=2, c=3)
