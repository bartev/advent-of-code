"""
A grid map

Author: Bartev
Date: 2024-12-10
"""

from rich import print as rprint


class Grid:
    def __init__(
        self, rows: int = None, cols: int = None, filename: str = None, default_val="."
    ):
        "A Basic grid"
        self.filename = filename
        if filename:
            self.grid = self.read_grid()
            self.rows = len(self.grid)
            self.cols = len(self.grid[0])
        else:
            self.rows = rows
            self.cols = cols
            self.grid = [[default_val for _ in range(cols)] for _ in range(rows)]

    def read_grid(self):
        """Read the grid from a file"""
        with open(self.filename, "r", encoding="utf8") as f:
            content = [list(line.strip()) for line in f]
        return content

    def print_grid(self) -> None:
        """Prints a 2D grid in a nicely formatted style."""
        for row in self.grid:
            rprint(" ".join(map(str, row)))

    def in_grid(self, row: int, col: int) -> bool:
        """True if row, col are within the grid"""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row: int, col: int):
        """Get the value at row, col"""
        if not self.in_grid(row, col):
            raise IndexError("Grid position out of bounds")
        return self.grid[row][col]

    def set(self, row: int, col: int, value):
        """Set a value at row, col"""
        if not self.in_grid(row, col):
            raise IndexError("Grid position out of bounds")
        self.grid[row][col] = value

    def __str__(self):
        """String representation of the grid."""
        return "\n".join(" ".join(map(str, row)) for row in self.grid)

    @staticmethod
    def manhattan_distance(r1, c1, r2, c2) -> int:
        """Calculate the manhattan distance between 2 points"""
        return abs(r2 - r1) + abs(c2 - c1)

    def all_m_distances(self, row_start, col_start):
        """Return the manhattan distance to all points from start"""
        mdist_grid = Grid(rows=self.rows, cols=self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                dist = self.manhattan_distance(row_start, col_start, row, col)
                mdist_grid.set(row, col, dist)
        return mdist_grid

    def positions_within_dist(self, row_start, col_start, distance: int):
        """Return all points within  manhattan distance from start"""
        points = []
        for row in range(self.rows):
            for col in range(self.cols):
                dist = self.manhattan_distance(row_start, col_start, row, col)
                if dist <= distance and not (row == row_start and col == col_start):
                    points.append((row, col))
        return points
