#!/usr/bin/env python

"""
Advent of code day 5

Author: Bartev
Date: 2024-12-04

Todays puzzle:

1. Read the data in 2 chunks, the rules, and the list of pages.
2. Always restrict the rules to those relevant to the current pages.
3. A single rule passes if the index of 1st number < index of 2nd number
4. All the rules pass if all relevant rules pass.

Part 1.
For every list of pages (a line in the 2nd half of input),
get the middle page number only if all the rules pass.
Return the sum of the middle numbers.

Part 2.

I made an assumption that all pages are connected by a rule to all
other pages.

I tested it by applying to all the data and seeing if I got the right
answer (I did)

I solved this problem 3 ways
1. Use networkx to create a DAG, and then do a topological sort on it.
2. Count the outputs and inputs from each page.
   Most outputs = first page
   2nd most outputs = 2nd page
   ...
   0 outputs = last page (= most inputs)
3. Don't assume all pages are connected by a rule
   Find rules that fail
   Fix each failure
   Find rules that still fail
   Repeat until no failures
"""

from collections import Counter
from pathlib import Path

import networkx as nx
from rich import print as rprint
from rich.panel import Panel
from rich.rule import Rule

from aoc.pyutils.utils import time_it

dname = Path("../../../../resources/2024/")
fname = dname / "d05.txt"
FNAME_TEST = "test_data.txt"


# ########## Part 1

rprint(Rule("Part 1", style="bold green"))
rprint(Panel.fit("[bold green]Part 1", style="bold green"))


def read_data(filename: str):
    """Read the data into rules and pages"""
    with open(filename, "r") as f:
        content = f.read()

    data1, data2 = content.strip().split("\n\n")

    # parse rules into list of tuples
    rules = [tuple(map(int, line.split("|"))) for line in data1.splitlines()]

    list_pages = [list(map(int, line.split(","))) for line in data2.splitlines()]
    return rules, list_pages


def relevant_rules(rules: list[tuple], pages: list[int]) -> list[tuple]:
    """return the list of rules that apply to the current pages
    (both before/after page must be in the rule)
    """
    return [rule for rule in rules if rule[0] in pages and rule[1] in pages]


def rule_passes(rule: tuple, pages: list[int]) -> bool:
    """true if the page order passes the rule"""
    before = rule[0]
    after = rule[1]
    return pages.index(before) < pages.index(after)


def apply_rules(rules: list[tuple], pages: list[int]) -> bool:
    """True if all the rules pass"""
    rel_rules = relevant_rules(rules, pages)
    pass_fail = [rule_passes(rule, pages) for rule in rel_rules]
    return all(pass_fail)


def middle_page(pages: list[int]) -> int:
    """Get the middle page from the list of pages
    Assumes there's an odd number of pages
    """
    return pages[(len(pages) - 1) // 2]


@time_it
def part1(filename: str) -> int:
    """Run part 1 given the input file
    Return value should be the solution"""
    rules, list_pages = read_data(filename)
    res = [middle_page(pages) for pages in list_pages if apply_rules(rules, pages)]
    return sum(res)


rprint(f"""test data: {part1(FNAME_TEST)}""")

rprint(f"""Problem input: {part1(fname)}""")

# ########## Part 2

rprint(Rule("Part 2", style="bold red"))
rprint(Panel.fit("[bold red]Part 2", style="bold red"))


def find_network(rules):
    """This assumes all nodes are covered by the rules
    This function could be more robust by adding all
    the pages as nodes, and all the edges as rules.

    Then, check that the graph is strongly_connected
    (see nx.strongly_connected_components)

    Also check that the number of nodes in the graph
    equals the len of the strongly connected component.
    """
    # Create directed graph
    graph = nx.DiGraph()
    graph.add_edges_from(rules)
    # Output the graph
    # print("Nodes:", graph.nodes())
    # print("Edges:", graph.edges())
    ordered_nodes = list(nx.topological_sort(graph))
    # print("Topological order:", ordered_nodes)
    return ordered_nodes


def fix_order(pages: list[int], rules: list[tuple]) -> list[int]:
    """Fix the order of the pages"""
    rel_rules = relevant_rules(rules, pages)
    # rprint(rel_rules)
    ordered_pages = find_network(rel_rules)
    # Make sure all the pages are covered by the rules
    # if a rule didn't specify a page number, then it
    # wouldn't be in ordered_pages
    assert all(page in ordered_pages for page in pages)
    return ordered_pages


@time_it
def part2(filename: str) -> int:
    """Run part 2 given the input file
    Return value should be the solution"""
    rules, list_pages = read_data(filename)
    bad_pages = [pages for pages in list_pages if not apply_rules(rules, pages)]
    fixed_pages = [fix_order(pages, rules) for pages in bad_pages]
    res = [middle_page(pages) for pages in fixed_pages]
    return sum(res)


rprint(f"""test data: {part2(FNAME_TEST)}""")
rprint(f"""Problem input: {part2(fname)}""")


rprint(Rule("Part 2b (no network)", style="bold yellow"))
rprint(Panel.fit("[bold yellow]Part 2b", style="bold yellow"))


def fix_order_no_network(pages: list[int], rules: list[tuple]) -> list[int]:
    """Find how many input/outputs there are from each node.
    Sort by outputs, and that is the order of items.
    This solution also assumes that every pair of nodes has a
    rule associated with it.
    """
    rel_rules = relevant_rules(rules, pages)
    outs = Counter()
    ins = Counter()
    for first, second in rel_rules:
        outs[first] += 1
        ins[second] += 1
    # rprint(f"outs: {outs.most_common()}")
    # rprint(f"ins: {ins.most_common()}")
    # `most_common()` sorts by frequency and converts to a list of
    # tuples (key, count)
    res = [x for x, y in outs.most_common()] + [ins.most_common()[0][0]]
    return res


@time_it
def part2b(filename: str) -> int:
    """Try part2 w/o networkx"""
    rules, list_pages = read_data(filename)
    bad_pages = [pages for pages in list_pages if not apply_rules(rules, pages)]
    fixed_pages = [fix_order_no_network(pages, rules) for pages in bad_pages]
    res = [middle_page(pages) for pages in fixed_pages]
    return sum(res)


rprint(f"""test data: {part2b(FNAME_TEST)}""")
rprint(f"""Problem input: {part2b(fname)}""")

rprint(Rule("Part 2c (incomplete rules ok)", style="bold blue"))
rprint(Panel.fit("[bold yellow]Part 2c", style="bold blue"))


def move_item(pages: list[int], idx_before: int, idx_after: int) -> list[int]:
    """move the item in index `from` to the index `to`"""
    if idx_before < idx_after:
        # rprint(f"Skipping rule, out of order")
        pass
    else:
        item = pages.pop(idx_before)
        pages.insert(idx_after, item)
    return pages


def fix_pages_rule(pages: list[int], rule: tuple) -> list[int]:
    """Fix pages for a single rule"""
    before, after = rule
    idx_before = pages.index(before)
    idx_after = pages.index(after)
    return move_item(pages, idx_before, idx_after)


def fix_pages_move(pages: list[int], rules: list[tuple]) -> list[int]:
    """Fix a set of pages by moving the page that cause it to fail a rule.
    pages is a single set of pages (1 line in the inputs)
    rules is the full set of rules (not all apply)
    """
    rel_rules = relevant_rules(rules, pages)
    # rprint(f"rules: {rel_rules}")
    failing_rules = [rule for rule in rel_rules if not rule_passes(rule, pages)]
    # Watch out for mutating a list in a loop.
    # In this case, the loop doesn't depend on pages, so I think it's ok
    if failing_rules:
        # Apply all fixes
        # Some may not be able to be applied after a previous move, but
        # will be fixed the next time around
        for rule in failing_rules:
            pages = fix_pages_rule(pages, rule)
        pages = fix_pages_move(pages, rel_rules)
    return pages


@time_it
def part2c(filename: str) -> int:
    """Solve even with incomplete rules"""
    rules, list_pages = read_data(filename)
    bad_pages = [pages for pages in list_pages if not apply_rules(rules, pages)]
    # rprint(f"bad_pages: {bad_pages}")
    # cur_page = bad_pages[2]
    # rprint(f"input: {cur_page}")
    # fixed_pages = fix_pages_move(cur_page, rules)
    # rprint(f"fixed: {fixed_pages}")
    fixed_pages = [fix_pages_move(pages, rules) for pages in bad_pages]
    res = [middle_page(pages) for pages in fixed_pages]
    return sum(res)


rprint(f"""test data: {part2c(FNAME_TEST)}""")
rprint(f"""Problem input: {part2c(fname)}""")
