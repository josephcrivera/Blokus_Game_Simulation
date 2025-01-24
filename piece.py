"""
Blokus shapes and pieces.

Modify only the methods marked as TODO.
"""
import copy
import textwrap
from typing import Optional

from shape_definitions import ShapeKind

# A point is represented by row and column numbers (r, c). The
# top-left corner of a grid is (0, 0). Note that rows/columns
# correspond to vertical/horizontal axes, respectively. So, we
# will typically index into a 2-dimensional grid using
# grid[r][c] (as opposed to grid[y][x]).
#
Point = tuple[int, int]


# We will typically unpack a Point as follows: (r, c) = point
# In other cases, the row and col functions may be helpful.
#
def row(point: Point) -> int:
    return point[0]


def col(point: Point) -> int:
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """
        squares = []
        real_squares = []
        origin = (0, 0)
        transform = False

        dedent_lines = textwrap.dedent(definition)
        lines = dedent_lines.split('\n')
        lines = list(filter(None, lines))

        for r, line in enumerate(lines):
            for c, character in enumerate(line):
                if character == "X":
                    Point = (r, c)
                    squares.append(Point)
                elif character == "O":
                    if transform == False:
                        transform = True
                    origin = (r, c)
                    squares.append(origin)
                elif character =="@":
                    if transform == False:
                        transform = True
                    origin = (r, c)
        # Point tuple keeps coordinates reverse order. Instead of (x, y), they
        # are kept as (y, x) so it's easier to index list[y][x] etc. Convention
        # also used the notion of r, c for rows and columns. 
        for point in squares:
            point_r, point_c = point
            origin_r, origin_c = origin
            new_point = (point_r - origin_r, point_c - origin_c)
            real_squares.append(new_point)

        return Shape(kind, origin, transform, real_squares)


    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        if self.can_be_transformed:
            for int, point in enumerate(self.squares):
                point_r, point_c = point
                new_point = (point_r, -point_c)
                self.squares[int]= new_point

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        if self.can_be_transformed:
            for int, point in enumerate(self.squares):
                point_r, point_c = point
                new_point = (-point_c, point_r)
                self.squares[int]= new_point

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        if self.can_be_transformed:  
            for int, point in enumerate(self.squares):
                point_r, point_c = point
                new_point = (point_c, -point_r)
                self.squares[int]= new_point


class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If true, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.shape.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.shape.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]

    def cardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None

        cardinal_positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = set()
        sqs = self.shape.squares

        for square in self.squares():
            for position in cardinal_positions:
                neighbor = (square[0] + position[0], square[1] + position[1])
                if neighbor not in self.squares():
                    neighbors.add(neighbor)
        return neighbors

    def intercardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None

        intercardinal_positions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        neighbors = set()

        for square in self.squares():
            for position in intercardinal_positions:
                neighbor = (row(square) + position[0], 
                            col(square) + position[1])
                if (neighbor not in self.cardinal_neighbors() and
                    neighbor not in self.squares()):
                        neighbors.add(neighbor)
        return neighbors