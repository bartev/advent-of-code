import functools
import re
from functools import cache
from pathlib import Path

import rich

dname = Path("../../../../resources/2024/")
fname = dname / "d19.txt"


input = "test_data.txt"
input = fname
with open(input) as f:
    ls = f.read().strip().split("\n")

stripes, _, *patterns = ls
stripes = stripes.split(", ")


# pattern is a string
# op is a function
@cache
def is_possible(pattern, op):
    return not pattern or op(
        is_possible(pattern[len(stripe) :], op)
        for stripe in stripes
        if pattern.startswith(stripe)
    )


for op in any, sum:
    print(sum(is_possible(pattern, op) for pattern in patterns))
