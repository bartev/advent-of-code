#!/usr/bin/env python

import logging
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

    def split_block(self, length_needed: int) -> list:
        """Split into a block of length: length_needed, and remainder
        for_head will be up to length_needed, with 0 spaces
        for_tail will be the original length - length_needed (no spaces since last block)

        Ex.
        need 10
        have 4
        still need 6 (max(0, 10-4))
        remain = 0 (max(0, 4-10))

        """
        still_needed = max(0, length_needed - self.length)
        remaining_in_tail = max(0, self.length - length_needed)
        length_fulfilled = min(length_needed, self.length)

        # rprint(self)
        # rprint(f"{still_needed=}, {remaining_in_tail=}, {length_fulfilled=}")

        for_head = (
            Block(self.index, length_fulfilled, 0) if length_fulfilled > 0 else None
        )
        for_tail = (
            Block(self.index, remaining_in_tail, 0) if remaining_in_tail > 0 else None
        )
        # still_needed
        return for_head, for_tail, still_needed


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
    return sum(idx * val for (idx, val) in enumerate(xs))


def fill_spaces(blocks: list) -> list:
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


def fill_spaces_2(blocks: list[Block]):
    """Take block 1, breakup last block if needed, append after block 1, keep other at end"""
    results_list = []

    # initialize the loop
    idx = 0
    len_blks = len(blocks)
    cur_block = blocks[idx]
    rest_blocks = blocks[idx + 1 :]
    results_list.append(cur_block)
    counter = 0
    # breakpoint()

    while idx < len_blks:
        # rprint(f"{counter=}, {idx=}")
        # rprint(blocks)
        if rest_blocks:
            needed = cur_block.spaces
            last_block = blocks[-1]
            for_head, for_tail, still_needed = last_block.split_block(needed)
            # rprint(f"{needed=}, {still_needed=}, {for_head=}, {for_tail=}")
            if for_head:
                results_list.append(for_head)
            # breakpoint()
            blocks = blocks[:-1]

            if for_tail:
                blocks.append(for_tail)  # replace the last block
            rest_blocks = blocks[idx + 1 :]

            cur_block.spaces = still_needed

            if still_needed == 0:
                idx += 1
                if idx >= len(blocks):
                    break
                cur_block = blocks[idx]
                results_list.append(cur_block)

        else:
            # breakpoint()
            break
        # if idx >= len_blks:
        #     breakpoint()

        counter += 1
    return results_list


def convert_to_list(blocks: list[Block]) -> list[int]:
    res = []
    for block in blocks:
        _id = block.index
        length = block.length
        res = res + [_id] * length
    return res


def get_hash_2(blocks: list[Block]):
    id_list = convert_to_list(blocks)
    return get_hash(id_list)


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""

    # This 1st way works for the test set, but not the actual data.
    if false:
        blocks1 = read_data(filename)
        # rprint(blocks1)
        indices1 = fill_spaces(blocks1)
        # rprint(indices1)
        rprint(get_hash(indices1))

    if true:
        rprint(Panel.fit("[bold blue]Part 1b"))
        blocks2 = read_data(filename)
        # rprint(blocks)
        indices2 = fill_spaces_2(blocks2)
        # rprint(f"{indices2=}")
        rprint(get_hash_2(indices2))


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
