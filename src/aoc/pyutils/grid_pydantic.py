# """
# A grid map, using pydantic and points


# Author: Bartev
# Date: 2024-12-14
# """

# import rich
# from pydantic import BaseModel, Field, FilePath, root_validator

# Point = tuple[int, int]  # (row, col)
# Region = list[Point]


# class Grid(BaseModel):
#     rows: int | None = Field(
#         None, init=False, gt=0, description="number rows in the grid"
#     )
#     cols: int | None = Field(
#         None, init=False, gt=0, description="number cols in the grid"
#     )
#     filename: FilePath | None = Field(None, init=False, description="file to read")
#     default_val: str = Field(".", description="default value for drawing grid cells")
#     grid: list = Field(default_factory=list, description="2D grid structure")

#     @root_validator(pre=True)
#     @classmethod
#     def initialize_grid(cls, values):
#         filename = values.get("filename")
#         rows = values.get("rows")
#         cols = values.get("cols")
#         default_val = values.get("default_val", ".")

#         if filename:
#             with open(filename, "r", encoding="utf8") as f:
#                 grid = [list(line.strip()) for line in f]
#             values["grid"] = grid
#             values["rows"] = len(grid)
#             values["cols"] = len(grid[0]) if grid else 0
#         else:
#             values["grid"] = [[default_val for _ in range(cols)] for _ in range(rows)]
#         return values

#     def print_grid(self) -> None:
#         """Prints the grid in a nicely formatted style."""
#         for row in self.grid:
#             rich.print(" ".join(map(str, row)))

#     def in_grid(self, point: tuple[int, int]) -> bool:
#         """True if row, col are within the grid."""
#         row, col = point
#         return 0 <= row < self.rows and 0 <= col < self.cols

#     def get(self, point: tuple[int, int]):
#         """Get the value at row, col."""
#         if not self.in_grid(point):
#             raise IndexError("Grid position out of bounds")
#         row, col = point
#         return self.grid[row][col]

#     def set(self, point: tuple[int, int], value):
#         """Set a value at row, col."""
#         if not self.in_grid(point):
#             raise IndexError("Grid position out of bounds")
#         row, col = point
#         self.grid[row][col] = value

#     def __str__(self):
#         """String representation of the grid."""
#         return "\n".join(" ".join(map(str, row)) for row in self.grid)
