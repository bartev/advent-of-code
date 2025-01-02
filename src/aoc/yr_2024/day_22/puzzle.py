#!/usr/bin/env python

import logging
from collections import defaultdict
from pathlib import Path

import rich
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
fname = dname / "d22.txt"
FNAME_TEST = "test_data.txt"


def read_data(filename: str | Path):
    """Read the data into rules and pages"""
    with open(filename, "r", encoding="utf8") as f:
        data = [int(line.strip()) for line in f]
    return data


# init_secrets = [1, 10, 100, 2024]


def print_bin_times(num: int):
    """Multipliying by 64 (2**6) adds 6 0's to the end of the string"""

    print(f"{num=}, {bin(num)=}")
    print(f"n=2, {bin(num * 2)=}")
    print(f"n=4, {bin(num * 4)=}")
    print(f"n=8, {bin(num * 8)=}")
    print(f"n=16, {bin(num * 16)=}")
    print(f"n=32, {bin(num * 32)=}")
    print(f"n=64, {bin(num * 64)=}")


# print_bin_times(3)


def print_bin_div(num: int):
    """Dividing by 32 (2**5) removes the last 5 binary digits"""
    print(f"{num=}, {bin(num)=}")
    print(f"n=2, {bin(num // 2)=}")
    print(f"n=4, {bin(num // 4)=}")
    print(f"n=8, {bin(num // 8)=}")
    print(f"n=16, {bin(num // 16)=}")
    print(f"n=32, {bin(num // 32)=}")


# print_bin_div(100)


def xor(x: int, y: int) -> int:
    """compute and print the binary xor

    Example
    >>> xor(5, 8)
    xor(5, 8)
    0101 : 5
    1000 : 8
    ---------
    1101 : 13
    13
    """
    res = x ^ y
    max_len = max(len(bin(x)), len(bin(y))) - 2
    format_str = f"0{max_len}b"
    # Print the binary representations
    print(f"{format(x, format_str)} : {x}")
    print(f"{format(y, format_str)} : {y}")
    print("-" * (max_len + 5))
    print(f"{format(res, format_str)} : {res}")
    return res


def mix(value: int, secret_num: int) -> int:
    """Mix a value into the secret_number

    1. Calc the bitwize xor of value and secret_num
    2. secret_num is the result of this operation
    """
    new_secret_num = value ^ secret_num
    return new_secret_num


def prune(secret_num: int) -> int:
    """result of modulo 16777216
    modulo is the remainder (%)
    """
    divisor = 16777216
    # 16777216 = 17471 * 3 * 2^5
    new_secret_num = secret_num % divisor
    return new_secret_num


def next_secret(secret_num: int) -> int:
    """Calculate the next secret number
    1. multiply by 64
    2. mix into secret_num
    3. prune
    4. div by 32
    5. mix into secret_num (orig or newest?)
    6. prune
    7. multiply by 2048 (= 2^11)
    8. mix into secret_num
    9. prune
    """
    step3a = prune(mix(secret_num * 64, secret_num))
    step6a = prune(mix(step3a // 32, step3a))
    step9a = prune(mix(step6a * 2048, step6a))
    return step9a


def get_nth_new_secret(start, n) -> int:
    """Return the nth new secret numbers"""
    secrets = {start}
    new_secret = start
    while len(secrets) <= n:
        new_secret = next_secret(new_secret)
        secrets.add(new_secret)
    # rich.print(secrets)
    return new_secret


def print_10(start: int):
    """Print 10 secret numbers in sequence"""
    print(start)
    new_secret = start
    for _ in range(10):
        new_secret = next_secret(new_secret)
        print(new_secret)


rich.print(Rule("Part 1", style="bold green"))
rich.print(Panel.fit("[bold green]Part 1"))


@time_it
def part1(fname: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    init_secrets = read_data(fname)
    res = {secret: get_nth_new_secret(secret, 2000) for secret in init_secrets}
    return sum(res.values())


# print_10(123)

#
rich.print(f"""test data: {part1(FNAME_TEST)}""")
# rich.print(f"""Problem input: {part1(fname)}""")

# # ########## Part 2


def get_price(secret: int) -> int:
    """The price is the last digit of the secret"""
    return secret % 10


def first_n_secrets(secret: int, n: int) -> list[int]:
    """Get the first n prices from secret"""
    secrets = [secret]
    while len(secrets) <= n:
        secret = next_secret(secret)
        if secret not in secrets:
            secrets.append(secret)
    return secrets


def first_n_prices(secret: int, n: int) -> list[int]:
    """Get the first n prices from secret"""
    secrets = [secret]
    prices = [get_price(secret)]
    while len(secrets) <= n:
        secret = next_secret(secret)
        if secret not in secrets:
            secrets.append(secret)
            prices.append(get_price(secret))
    return prices


def get_deltas(prices: list[int]):
    """Get the difference btw consecutive prices"""
    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    return deltas


def combine_dicts(dicts):
    """Combine the list of dicts by summing the values"""
    combined = defaultdict(int)
    for d in dicts:
        for key, value in d.items():
            combined[key] += value
    return dict(combined)


def process_secret(secret: int, n: int):
    """Do everything for a single secret."""
    prices = first_n_prices(secret, n)  # convert secrets to prices
    deltas = get_deltas(prices)  # convert prices to deltas

    # Print the formatted output
    if False:
        secrets = first_n_secrets(secret, n)  # Generate a sequence of secrets
        for sec, pri, delta in zip(secrets, prices, [None] + deltas):
            if delta is None:
                print(f"{sec:>9}: {pri}")
            else:
                print(f"{sec:>9}: {pri} ({delta:+})")

    # create a list of (price, prev-4-deltas)
    # use None for unavailable deltas
    extended_deltas = [None] + deltas
    # rich.print(extended_deltas)

    price_delta_pairs = [
        (price, tuple(extended_deltas[i - 3 : i + 1]))
        for i, price in enumerate(prices)
        if i >= 4
    ]

    # rich.print(price_delta_pairs)

    first_seq_price = {}
    for price, prev_deltas in price_delta_pairs:
        if prev_deltas not in first_seq_price:
            first_seq_price[prev_deltas] = price

    return first_seq_price


rich.print(Rule("Part 2", style="bold red"))
rich.print(Panel.fit("[bold red]Part 2"))


@time_it
def part2(fname: str, n: int):
    """Run part 2 given the input file
    Return value should be the solution"""
    init_secrets = read_data(fname)
    # init_secret, to_match, expected_price = 1, (-2, 1, -1, 3), 7
    # init_secret, to_match, expected_price = 2, (-2, 1, -1, 3), 7
    # init_secret, to_match, expected_price = 3, (-2, 1, -1, 3), None
    # init_secret, to_match, expected_price = 2024, (-2, 1, -1, 3), 9
    # first_seq_price = process_secret(init_secret, n)
    # rich.print(first_seq_price)

    first_seq_prices = [process_secret(secret, n) for secret in init_secrets]
    sum_seq_prices = combine_dicts(first_seq_prices)
    # rich.print(sum_seq_prices)
    max_elem = max(sum_seq_prices.items(), key=lambda x: x[1])
    rich.print(max_elem)
    return max_elem


part2(FNAME_TEST, 2000)
# rich.print(f"""test data: {part2(FNAME_TEST, 50)}""")
# rich.print(f"""Problem input: {part2(fname, 2000)}""")
