"""
This solution is slower than the others.
I'm not sure why.
"""

import functools
import re
from functools import cache
from pathlib import Path

import rich

dname = Path("../../../../resources/2024/")
fname = dname / "d19.txt"


# PART 1
s = [s.splitlines() for s in open("test_data.txt").read().split("\n\n")]
s = [s.splitlines() for s in open(fname).read().split("\n\n")]

# open("test_data.txt").read().split("\n\n")
# Returns 2 lists
# The first one is a single string 'r, wr, ...'
# The 2nd one is each of the designs

pp, dd = s[0][0].split(", "), s[1]

pat = "(" + "|".join(pp) + ")*"

res = [re.fullmatch(pat, s) for s in dd]
rich.print(res)


# PART 2


import functools

s = [s.splitlines() for s in open("test_data.txt").read().split("\n\n")]
pp, dd = s[0][0].split(", "), s[1]


@functools.cache
def c(d):
    return 1 if d == "" else sum(c(d[len(p) :]) for p in pp if d.startswith(p))


print(sum(c(d) for d in dd))
