"""
A grid map

Author: Bartev
Date: 2024-12-10
"""

from rich import print as rprint
from aoc.pyutils.utils import (
    find_continuous_values,
    find_continuous_values_ge,
    find_continuous_values_le,
    series_from,
)

Point = tuple[int, int]  # (row, col)
Region = list[Point]


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

    def in_grid(self, point: Point) -> bool:
        """True if row, col are within the grid"""
        row, col = point
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, point: Point):
        """Get the value at row, col"""
        if not self.in_grid(point):
            raise IndexError("Grid position out of bounds")
        row, col = point
        return self.grid[row][col]

    def set(self, point: Point, value):
        """Set a value at row, col"""
        if not self.in_grid(point):
            raise IndexError("Grid position out of bounds")
        row, col = point
        self.grid[row][col] = value

    def __str__(self):
        """String representation of the grid."""
        return "\n".join(" ".join(map(str, row)) for row in self.grid)

    @staticmethod
    def manhattan_distance(point1: Point, point2: Point) -> int:
        """Calculate the manhattan distance between 2 points"""
        r1, c1 = point1
        r2, c2 = point2
        return abs(r2 - r1) + abs(c2 - c1)

    def all_m_distances(self, point_start: Point):
        """Return the manhattan distance to all points from start"""
        row_start, col_start = point_start
        mdist_grid = Grid(rows=self.rows, cols=self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                dist = self.manhattan_distance((row_start, col_start), (row, col))
                mdist_grid.set((row, col), dist)
        return mdist_grid

    def positions_within_dist(self, point_start: Point, distance: int):
        """Return all points within  manhattan distance from start"""
        row_start, col_start = point_start
        points = []
        # Don't search the entir grid every time
        row_min = max(0, row_start - distance)
        row_max = min(row_start + distance, self.rows - 1)
        col_min = max(0, col_start - distance)
        col_max = min(col_start + distance, self.cols - 1)
        # breakpoint()

        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                dist = self.manhattan_distance((row_start, col_start), (row, col))
                # rprint(f"{row=}, {col=}, {dist=}, {distance=}")
                if dist <= distance and not (row == row_start and col == col_start):
                    # rprint("appending {row, col}")
                    points.append((row, col))
        return points

    def print_positions(self, region: Region):
        """Print the grid with only the positions shown"""
        pos_grid = Grid(rows=self.rows, cols=self.cols)
        for point in region:
            val = self.get(point)
            pos_grid.set(point, val)
        return pos_grid

    def print_on_grid(self, region: Region, char: str = "X"):
        """Print `chr` for every point in region"""
        assert len(char) == 1
        pos_grid = Grid(rows=self.rows, cols=self.cols)
        for point in region:
            pos_grid.set(point, char)
        return pos_grid

    def region_boundaries(self, region: Region) -> tuple[Point]:
        """Get the min/max row/col in the region.
        This defines the rectangular region that surrounds the region"""
        max_row = max(row for row, col in region)
        min_row = min(row for row, col in region)
        max_col = max(col for row, col in region)
        min_col = min(col for row, col in region)
        return (min_row, min_col), (max_row, max_col)

    def find_top_row_points(self, region: Region) -> Region:
        """Find all the points in the top row of `region`"""
        point_min, _ = self.region_boundaries(region)
        row_min, _ = point_min
        return [(row, col) for (row, col) in region if row == row_min]

    def find_bottom_row_points(self, region: Region) -> Region:
        """Find all the points in the bottom row of `region`"""
        _, point_max = self.region_boundaries(region)
        row_max, _ = point_max
        return [(row, col) for (row, col) in region if row == row_max]

    def find_left_col_points(self, region: Region) -> Region:
        """Find all the points in the leftmost col of `region`"""
        point_min, _ = self.region_boundaries(region)
        _, col_min = point_min
        return [(row, col) for (row, col) in region if col == col_min]

    def find_right_col_points(self, region: Region) -> Region:
        """Find all the points in the rightmost row of `region`"""
        _, point_max = self.region_boundaries(region)
        _, col_max = point_max
        return [(row, col) for (row, col) in region if col == col_max]

    def point_below(self, point: Point) -> Point | None:
        """Get the point below point, if in the grid"""
        row, col = point
        return (row + 1, col) if row < self.rows else None

    def point_above(self, point: Point) -> Point | None:
        """Get the point below point, if in the grid"""
        row, col = point
        return (row - 1, col) if row > 0 else None

    def point_left(self, point: Point) -> Point | None:
        """Get the point to the left of point, if in the grid"""
        row, col = point
        return (row, col - 1) if col > 0 else None

    def point_right(self, point: Point) -> Point | None:
        """Get the point to the right of point, if in the grid"""
        row, col = point
        return (row, col + 1) if col < self.cols else None

    def drop_adjacent_points_down(self, points, region) -> Region:
        """Drop all adjacent points downward for each point in region.
        Returns a new Region
        """
        # initialize the result
        res_region = region.copy()
        for point in points:
            row_start, col_start = point
            rows_in_col = [row for (row, col) in region if col == col_start]
            rows_to_drop = find_continuous_values_ge(row_start, rows_in_col)
            for row in rows_to_drop:
                res_region.discard((row, col_start))
        return res_region

    def drop_adjacent_points_right(self, points, region) -> Region:
        """Drop all adjacent points going right for each point in region.
        Returns a new Region
        """
        # initialize the result
        res_region = region.copy()
        for point in points:
            row_start, col_start = point
            cols_in_row = [col for (row, col) in region if row == row_start]
            cols_to_drop = find_continuous_values_ge(col_start, cols_in_row)
            for col in cols_to_drop:
                res_region.discard((row_start, col))
        return res_region

    def drop_adjacent_points_up(self, points, region) -> Region:
        """Drop all adjacent points downward for each point in region.
        Returns a new Region
        """
        # initialize the result
        res_region = region.copy()
        for point in points:
            row_start, col_start = point
            rows_in_col = [row for (row, col) in region if col == col_start]
            # Note the different direction from down (le vs ge)
            rows_to_drop = find_continuous_values_le(row_start, rows_in_col)
            for row in rows_to_drop:
                res_region.discard((row, col_start))
        return res_region

    def drop_adjacent_points_left(self, points, region) -> Region:
        """Drop all adjacent points going right for each point in region.
        Returns a new Region
        """
        # initialize the result
        res_region = region.copy()
        for point in points:
            row_start, col_start = point
            cols_in_row = [col for (row, col) in region if row == row_start]
            # Note the different direction from right (le vs ge)
            cols_to_drop = find_continuous_values_le(col_start, cols_in_row)
            for col in cols_to_drop:
                res_region.discard((row_start, col))
        return res_region
