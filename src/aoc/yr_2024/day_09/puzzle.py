#!/usr/bin/env python

import logging
from collections import deque, namedtuple
from pathlib import Path

from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

# Set up basic config for logging
FORMAT = "%(levelname)8s - %(funcName)s - %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, handlers=[RichHandler()])
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

dname = Path("../../../../resources/2024/")
fname = dname / "d09.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str):
    """Read the data into a list of tuples, 2 char at a time"""
    with open(filename, "r") as f:
        # input has odd number of chars, add 0 spaces at the end.
        data = f.read().strip() + "0"
        # rprint(data)
        # rprint(f"{len(data)}")
        pairs = []
        assert len(data) % 2 == 0  # make sure even number of items
        for i in range(0, len(data), 2):
            length, spaces = data[i : i + 2]
            pairs.append(Block(i // 2, int(length), int(spaces)))
        # rprint(pairs)
    return pairs


class Block:
    def __init__(self, index: int, length: int, spaces: int):
        "docstring"
        self.index = index
        self.length = length
        self.spaces = spaces

    def __repr__(self):
        """Provide a detailed string representation for debugging."""
        return f"Block(index={self.index}, length={self.length}, spaces={self.spaces})"

    def __str__(self):
        """Provide a user-friendly string representation."""
        return f"Block {self.index}: Length={self.length}, Spaces={self.spaces}"

    def remove_n_from_end(self, n: int) -> dict:
        """return a list of length n indices
        Remove the same number from the length from the length
        of the current block
        """
        to_return = min(n, self.length)
        needed = n - to_return
        logger.debug(f"{n=}, {to_return=}, {needed=}")
        indices = [self.index] * to_return
        self.length -= to_return
        return {"indices": indices, "needed": needed}


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1"))


# def add_next_block(d_map: list[int], blocks: deque):
#     """Add the first block in the list to the disk_map"""
#     first_block = blocks.pop(0)
#     logger.debug(f"{first_block=}")
#     end_block = blocks.pop()
#     logger.debug(f"{end_block=}")
#     logger.debug(f"{first_block.index=}")
#     indices = [first_block.index] * first_block.length
#     # rprint(blocks)
#     logger.debug(f"{len(blocks)=}")
#     logger.debug(f"{first_block.spaces=}")
#     if len(blocks) > 0:
#         res_dict = end_block.remove_n_from_end(first_block.spaces)
#         logger.debug(res_dict)
#         indices = indices + res_dict["indices"]
#         needed = res_dict["needed"]
#         if needed > 0:
#             logger.debug(f"{end_block=}")
#             logger.debug(f"{needed=}")
#             blocks.append(end_block)
#     d_map = d_map + indices
#     # rprint(blocks)
#     logger.debug(f"{d_map=}")
#     return d_map, blocks


def remove_empty_blocks_from_end(blocks) -> list[Block]:
    """remove all blocks from the end with length=0"""
    lengths = [block.length for block in blocks]
    count = 0
    logger.debug(lengths)
    for num in reversed(lengths):
        if num == 0:
            count += 1
        else:
            break
    return blocks[:-count] if count > 0 else blocks


def add_n_from_end(d_map: list[int], n: int, blocks: list[Block]):
    """add n indices from the end of blocks"""
    num_blocks = len(blocks)
    needed = n
    cur_block = 1  # from end
    while num_blocks > 0 and needed > 0:
        logger.debug(f"{num_blocks}, {needed=}")
        end_block = blocks[-cur_block]
        logger.debug(end_block)
        logger.debug(pretty_str(d_map))
        # breakpoint()
        res_dict = end_block.remove_n_from_end(needed)
        new_indices = res_dict["indices"]
        d_map = d_map + new_indices
        needed = res_dict["needed"]
        if needed == 0:
            num_blocks -= 1  # keep track of how many blocks there were
        cur_block += 1
    # rprint(blocks)
    blocks = remove_empty_blocks_from_end(blocks)
    logger.debug("just removed empty blocks from end")
    # rprint(blocks)
    return d_map, blocks


def pretty_str(xs: list[int]):
    """pretty print strin d_map"""
    return "".join(map(str, xs))


def get_hash(xs: list[int]):
    """Return the hash
    sum(idx * value)
    """
    return sum([idx * val for idx, val in enumerate(xs)])


def fill_spaces(blocks: deque) -> list:
    """Fill disk_map spaces with indices from the last block in the list"""
    d_map = []
    # d_map, blocks = add_next_block(d_map, blocks)
    # n = blocks[0].spaces
    for idx_cur_block in range(len(blocks)):
        logger.debug(f"iter: {idx_cur_block} to fill spaces")
        if idx_cur_block + 1 == len(blocks):
            # end case
            cur_block = blocks[idx_cur_block]
            logger.debug("last block")
            # Just add the current values (if I use add_n..., I'll add current values AND spaces)
            d_map = d_map + [cur_block.index] * cur_block.length
            logger.debug(f"After dmap: {pretty_str(d_map)}")

        elif idx_cur_block + 1 < len(blocks):
            cur_block = blocks[idx_cur_block]
            logger.debug(f"{cur_block=}")
            d_map = d_map + [cur_block.index] * cur_block.length
            logger.debug(f"before dmap {d_map}")
            d_map, blocks = add_n_from_end(d_map, cur_block.spaces, blocks)
            logger.debug(f"After dmap: {d_map}")
            # rprint(blocks)
        else:
            logger.debug(f"Exiting at {idx_cur_block=}")
            break
    return d_map


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    blocks = read_data(filename)
    # rprint(blocks)
    indices = fill_spaces(blocks)
    # rprint(pretty_str(indices))
    return get_hash(indices)


rprint(f"""test data: {part1(FNAME_TEST)}""")

# expected:
# 0099811188827773336446555566
# 0099811188827773336446555566
# 0099811188827773336446555566
# 00998111888277733364465555666
rprint(f"""Problem input: {part1(fname)}""")  #

# Too high
# 6333755670239

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2"))


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""


# rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")
