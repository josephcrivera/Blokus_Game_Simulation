import pytest
from typing import Optional, List, Tuple

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from fakes import BlokusFake
from blokus import Blokus


Cell = Optional[Tuple[int, str]]
Grid = List[List[Cell]]



def init_blokus_mini(num_players: int) -> BlokusBase:
    """
    makes a mini blokus game
    Inputs:
        num_players [int]: num of players
    Output:
        [BlokusBase]: a blokus game
    """
    return Blokus(num_players, 5, {(0, 0), (4, 4)})




def grid_to_string(grid: Grid) -> str:
    """
    Converts a grid to a string
    Inputs:
        grid [Grid]: a grid
    Output:
        [str]: string representation of the grid
    """
    size = len(grid)
    border = "+" + "-" * (size * 2) + "+\n"
    grid_str = border
    for row in grid:
        row_str = "|"
        for cell in row:
            if cell is None:
                row_str += "  "
            else:
                player, shape = cell
                print(shape)
                if player == 1:
                    row_str += shape.value + " "
                elif player == 2:
                    row_str += " " + shape.value
        row_str += "|\n"
        grid_str += row_str
    grid_str += border
    return grid_str

def string_to_grid(s: str) -> Grid:
    """
    Converts a string to a grid
    Inputs:
        s [str]: a string
    Output:
        [Grid]: the grid
    """
    lines = s.strip().split("\n")
    size = (len(lines[0]) - 2) // 2
    grid: Grid = []

    for line in lines[1:-1]:
        row = []
        cell_str = line[1:-1]
        for j in range(size):
            cell = cell_str[j*2:j*2+2]
            if cell.strip():
                if cell[0] != ' ':
                    row.append((1, ShapeKind(cell[0])))
                else:
                    row.append((2, ShapeKind(cell[1])))
            else:
                row.append(None)
        grid.append(row)
    #print(ShapeKind("1"))
    return grid

# Helper function to strip dedent
def dedent(text: str) -> str:
    """
    Dedents the string
    Inputs:
        text[str]: a string
    Output:
        [str]: string representation of the grid
    """
    import textwrap
    return textwrap.dedent(text).strip()


def test_grid_1() -> None:
    """
    Test 1
    """
    blokus = init_blokus_mini(2)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    piece_one.set_anchor((4, 4))
    blokus.maybe_place(piece_one)

    grid = blokus.grid
    s = """
        +----------+
        |1         |
        |          |
        |          |
        |          |
        |         1|
        +----------+
    """
    assert dedent(s).strip() == grid_to_string(grid).strip()
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_2() -> None:
    """
    Test 2
    """
    blokus = init_blokus_mini(2)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    piece_one.set_anchor((4, 4))
    blokus.maybe_place(piece_one)
    piece_two.set_anchor((1, 1))
    blokus.maybe_place(piece_two)
    piece_two.set_anchor((3, 2))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
        +----------+
        |1         |
        |  2 2     |
        |          |
        |     2 2  |
        |         1|
        +----------+
    """
    assert dedent(s).strip() == grid_to_string(grid).strip()
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_3() -> None:
    """
    Test 3
    """
    blokus = Blokus(2, 6, {(0, 0), (5, 5)})
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    piece_one.set_anchor((5, 5))
    blokus.maybe_place(piece_one)
    piece_two.set_anchor((1, 1))
    blokus.maybe_place(piece_two)
    piece_two.set_anchor((4, 3))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
        +------------+
        |1           |
        |  2 2       |
        |            |
        |            |
        |       2 2  |
        |           1|
        +------------+
    """
    assert dedent(s).strip() == grid_to_string(grid).strip()
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_4() -> None:
    """
    Test 4
    """
    blokus = Blokus(2, 7, {(0, 0), (6, 6)})
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    piece_one.set_anchor((6, 6))
    blokus.maybe_place(piece_one)
    piece_two.set_anchor((1, 1))
    blokus.maybe_place(piece_two)
    piece_two.set_anchor((5, 4))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
        +--------------+
        |1             |
        |  2 2         |
        |              |
        |              |
        |              |
        |         2 2  |
        |             1|
        +--------------+
    """
    assert dedent(s).strip() == grid_to_string(grid).strip()
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_5() -> None:
    """
    Test 5
    """
    blokus = Blokus(2, 8, {(0, 0), (7, 7)})
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    piece_one.set_anchor((7, 7))
    blokus.maybe_place(piece_one)
    piece_two.set_anchor((1, 1))
    blokus.maybe_place(piece_two)
    piece_two.set_anchor((6, 5))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
        +----------------+
        |1               |
        |  2 2           |
        |                |
        |                |
        |                |
        |                |
        |           2 2  |
        |               1|
        +----------------+
    """
    assert dedent(s).strip() == grid_to_string(grid).strip()
    assert grid == string_to_grid(grid_to_string(grid))
