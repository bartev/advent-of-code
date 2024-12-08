"""
Position class for puzzles

Author: Bartev
Date: 2024-12-07
"""


class Position:
    """A position object"""

    def __init__(self, row: int, col: int):
        "A position defined by (row, column)"
        self.row = row
        self.col = col

    def to_tuple(self):
        """Return position as a tuple"""
        return self.pos

    @property
    def pos(self):
        """Return the current position as a tuple"""
        return (self.row, self.col)

    def __add__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, tuple) and len(other) != 2:
            raise TypeError("Can only add a Position or a tuple of length 2")
        if isinstance(other, tuple):
            other = Position(other[0], other[1])
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, tuple) and len(other) != 2:
            raise TypeError("Can only add a Position or a tuple of length 2")
        if isinstance(other, tuple):
            other = Position(other[0], other[1])
        return Position(self.row - other.row, self.col - other.col)

    def lt(self, other, direction: tuple[int, int]) -> bool:
        """Compare to positions based on a direction vector.
        Uses a projection on the direction vector."""

        if isinstance(other, Position):
            other_row, other_col = other.row, other.col
        elif isinstance(other, tuple) and len(direction) == 2:
            other_row, other_col = other
        else:
            raise TypeError("Can only compare with another Position or a tuple")

        # Compute dot product with direction for comparison
        projection_self = self.row * direction[0] + self.col * direction[1]
        projection_other = other_row * direction[0] + other_col * direction[1]

        return projection_self < projection_other

    def __repr__(self):
        """Provide a string representation of the position."""
        return f"Position(row={self.row}, column={self.col})"
