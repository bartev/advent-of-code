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

    @classmethod
    def from_tuple(cls, tup):
        """Create a Position from a tuple"""
        if not isinstance(tup, tuple) or len(tup) != 2:
            raise TypeError("Input must be a tuple of 2 integers")
        return cls(*tup)

    @classmethod
    def sort_positions(cls, positions: list) -> list:
        """Sort a list of positions by row then col"""
        return sorted(positions, key=lambda pos: (pos.row, pos.col))

    @property
    def pos(self):
        """Return the current position as a tuple"""
        return (self.row, self.col)

    def __eq__(self, other):
        """Check for equality based on row and column"""
        if isinstance(other, tuple):
            other = self.from_tuple(other)
        if isinstance(other, Position):
            res = self.row == other.row and self.col == other.col
        else:
            res = False
        return res

    def __hash__(self):
        """Make Position hashable by combining row and col.
        This will allow me to create a set"""
        return hash((self.row, self.col))

    def __add__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, tuple):
            other = self.from_tuple(other)
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        """Add another position or tuple to this position"""
        if isinstance(other, tuple):
            other = self.from_tuple(other)
        return Position(self.row - other.row, self.col - other.col)

    def __mul__(self, other):
        """Scalar multiplication (int) or element-wise product (Position)"""
        if isinstance(other, Position):
            # dot product
            res = Position(self.row * other.row, self.col * other.col)
        elif isinstance(other, int):
            res = Position(self.row * other, self.col * other)
        else:
            raise TypeError("Multiplication only supported for int and Position (dot)")
        return res

    def dot(self, other) -> int:
        """Dot product between 2 Positions"""
        if not isinstance(other, Position):
            raise TypeError("Dot product is only supported for Position")
        return self.row * other.row * self.col * other.col

    def lt(self, other, direction: tuple[int, int]) -> bool:
        """Compare to positions based on a direction vector.
        Uses a projection on the direction vector."""
        if isinstance(other, tuple):
            other = self.from_tuple(other)
        # Compute dot product with direction for comparison
        projection_self = self.row * direction[0] + self.col * direction[1]
        projection_other = other.row * direction[0] + other.col * direction[1]

        return projection_self < projection_other

    def __repr__(self):
        """Provide a string representation of the position."""
        return f"Position(row={self.row}, column={self.col})"
