"""Utility functions for reading from a file."""


def read_file_to_lists(fname, delimiter=","):
    """Read a text file with unknown num of columns to lists"""
    column_lists = []
    with open(fname, "r") as f:
        for line in f:
            row = line.strip().split(delimiter)
            for i in range(len(row)):
                if i >= len(column_lists):
                    column_lists.append([])
                column_lists[i].append(row[i])
    return column_lists
