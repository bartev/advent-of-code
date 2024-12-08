"""
A Basic puzzle map object

Author: Bartev
Date: 2024-12-07
"""

from rich import print as rprint


class PuzzleMap:
    """A puzzle with basic methods"""

    DIRECTIONS = ["^", ">", "v", "<"]
    OBSTACLE = "#"
    INCREMENTS = dict(zip(DIRECTIONS, [(-1, 0), (0, 1), (1, 0), (0, -1)]))

    def __init__(self, filename: str):
        "docstring"
        self.labmap = self.read_grid(filename)
        self.min_row = 0
        self.min_col = 0
        self.max_row = len(self.labmap) - 1
        self.max_col = len(self.labmap[0]) - 1

    def read_grid(self, filename: str) -> list[str]:
        """Read the data into a list of strings"""
        with open(filename, "r") as f:
            content = [line.strip() for line in f]
        return content

    def replace_char(self, s: str, n: int, ch: str):
        """Replace the char at string index `n` with ch"""
        if n < 0 or n >= len(s):
            raise ValueError(f"n ({n}) is out of range")
        return s[:n] + ch + s[n + 1 :]

    def draw_map(
        self,
        filename: str = None,
        labmap: list[str] = None,
    ):
        """Draw map with new obstacles"""
        mylabmap = labmap if labmap else self.labmap.copy()
        if filename:
            with open(filename, "w") as f:
                for line in mylabmap:
                    f.write(line + "\n")
        else:
            for line in mylabmap:
                rprint(line)
        print()
