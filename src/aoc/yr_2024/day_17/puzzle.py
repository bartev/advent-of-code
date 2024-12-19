#!/usr/bin/env python

import logging
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, validator
from rich import print as rprint
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
fname = dname / "d17.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
    return content


# ########## Part 1


class OpComputer(BaseModel):
    program: list[int] = Field(
        default_factory=list, description="A list of integers where 0 <= n < 8"
    )
    a: int = Field(default=0, description="Register A")
    b: int = Field(default=0, description="Register B")
    c: int = Field(default=0, description="Register C")

    instr_ptr:int = Field(default=0, "position in program from where the next opcode is read")

    # Custom validator for the program field
    @validator("program", each_item=True)
    @classmethod
    def check_program_values(cls, value):
        if not (0 <= value < 8):
            raise ValueError("All integers in 'program' must satisfy 0 <= n < 8")
        return value


    def opcode(self):
        """the current opcode"""
        if self.instr_ptr < len(self.program) - 1:
            return self.program[self.instr_ptr]

    def operand(self):
        """the current operand"""
        if self.instr_ptr < len(self.program) - 1:
            return self.program[self.instr_ptr + 1]



rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""


rprint(f"""test data: {part1(FNAME_TEST)}""")
# rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


# @time_it
# def part2(filename: str) -> int:
#     """Run part 2 given the input file
#     Return value should be the solution"""


# # rprint(f"""test data: {part2(FNAME_TEST)}""")
# rprint(f"""Problem input: {part2(fname)}""")
