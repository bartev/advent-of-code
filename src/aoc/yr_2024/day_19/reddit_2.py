from functools import cache
from pathlib import Path

dname = Path("../../../../resources/2024/")
fname = dname / "d19.txt"

# P, _, *D = open("test_data.txt").read().splitlines()
P, _, *D = open(fname).read().splitlines()


@cache
def count(d):
    return d == "" or sum(
        count(d.removeprefix(p)) for p in P.split(", ") if d.startswith(p)
    )


# sum over bools gives a count of existence
# sum over ints counts all the different ways to make a design
for type in bool, int:
    print(sum(map(type, map(count, D))))
