from abc import ABC, abstractmethod
from typing import Optional

from base import BlokusBase
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from shape_definitions import definitions

Cell = Optional[tuple[int, ShapeKind]]
Grid = list[list[Cell]]

class Blokus(BlokusBase):
    """
    Blokus class to be implemented for testing later
    """
    _num_players: int
    _size: int
    _start_positions: set[Point]
    _shapes: dict[ShapeKind, Shape]
    _curr_player: int
    _grid: Grid
    _num_moves: int
    _retired_players: set
    _all_shapes: dict

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Subclasses should have constructors which accept these
        same first three arguments:

            num_players: Number of players
            size: Number of squares on each side of the board
            start_positions: Positions for players' first moves

        Raises ValueError...
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players.

        Note: This base class constructor does not raise the
        exceptions above, but subclass constructors should.
        """
        # super().__init__(num_players, size, start_positions)
        # if self._num_players != 1 and self._num_players != 2:
        #     raise NotImplementedError("PLEASE CHOOSE 1 OR 2 PLAYERS!")
        if num_players < 1 or num_players > 4:
            raise ValueError
        if size < 5:
            raise ValueError
        for position in start_positions:
            for val in position:
                if val < 0 or val > size - 1:
                    raise ValueError
        if len(start_positions) < num_players:
            raise ValueError
        self._grid = [[None] * size for _ in range(size)]
        self._num_players = num_players
        self._size = size
        self._start_positions = start_positions
        self._retired_players = set()
        self._all_shapes = {}
        self._curr_player = 1
        self._num_moves = 0
        self._played_pieces = []
    #
    # PROPERTIES
    #

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all 21 Blokus shapes, as named and defined by
        the string representations in shape_definitions.py.

        The squares and origin, if any, of each shape should
        correspond to the locations and orientations defined
        in shape_definitions. For example, the five-square
        straight piece is called ShapeKind.FIVE, defined as a
        vertical line (as opposed to horizontal), and has its
        origin at the middle (third) square.

        See shape_definitions.py for more details.
        """
        for int, shape in enumerate(definitions):
            shape_name = "shape_" + str(int)
            shape_name = Shape.from_string(shape, definitions[shape])
            self._all_shapes.update({shape_name.kind: shape_name})

        return self._all_shapes

    @property
    def size(self) -> int:
        """
        Returns the board size (the number of squares per side).
        """
        return (self._size)

    @property
    def start_positions(self) -> set[Point]:
        """
        Returns the start positions.
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        Returns the number of players. Players are numbered
        consecutively, starting from 1.
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "Whose turn is it?"). While the
        game is ongoing, this property never refers to a player
        that has played all of their pieces or that retired
        before playing all of their pieces. If the game is over,
        this property will not return a meaningful value.
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        Returns the set of players who have retired. These
        players do not get any more turns; they are skipped
        over during subsequent gameplay.
        """
        return self._retired_players

    @property
    def grid(self) -> Grid:
        """
        Returns the current state of the board (i.e. Grid).
        There are two values tracked for each square (i.e. Cell)
        in the grid: the player number (an int) who has played
        a piece that occupies this square; and the shape kind
        of that piece. If no played piece occupies this square,
        then the Cell is None.
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        Returns whether or not the game is over. A game is over
        when every player is either retired or has played all
        their pieces.
        """
        if len(self._retired_players) == self._num_players:
            return True

        if len(self._retired_players) == 1 and self._num_players == 2:
            if len(self.remaining_shapes(self.curr_player)) == 0:
                return True

        done = 0
        for num in range(1, self.num_players + 1):
            if len(self.remaining_shapes(num)) == 0:
                done += 1
        if (done + (len(self._retired_players))) == self.num_players:
            return True
        else:
            return False

    @property
    def winners(self) -> Optional[list[int]]:
        """
        Returns the (one or more) players who have the highest
        score. Returns None if the game is not over.
        """
        winners_lst = []
        high_score = -999
        if self.game_over:
            for player in range(1, self.num_players + 1):
                curr_score = self.get_score(player)
                high_score = max(high_score, curr_score)

            for player in range(1, self.num_players + 1):
                curr_score = self.get_score(player)
                if curr_score == high_score:
                    winners_lst.append(player)
            return winners_lst

        return None

    #
    # METHODS
    #

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns a list of shape kinds that a particular
        player has not yet played.
        """
        played_shapes = set()
        for row in self.grid:
            for cell in row:
                if cell is not None and cell[0] == player:
                    played_shapes.add(cell[1])

        remaining_shapes_list = []
        for shape in self.shapes.keys():
            if shape not in played_shapes:
                remaining_shapes_list.append(shape)
        return remaining_shapes_list

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall. For the purposes of this
        predicate, a "wall collision" occurs when at
        least one square of the piece would be located
        beyond the bounds of the (size x size) board.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        squares = piece.squares()
        for square in squares:
            row, col = square
            if row < 0 or col < 0 or row >= self.size or col >= self.size:
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall or with any played pieces.
        A "collision" between pieces occurs when they
        overlap.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        if not self.any_wall_collisions(piece):
            piece._check_anchor()
            locs = piece.squares()
            for row, col in locs:
                if self.grid[row][col] is not None:
                    return True
            return False
        else:
            return True

    def legal_to_place(self, piece: Piece) -> bool:
        """
        If the current player has not already played
        this shape, this method returns a boolean
        indicating whether or not the given piece is
        legal to place. This requires that:

         - if the player has not yet played any pieces,
           this piece would cover a start position;
         - the piece would not collide with a wall or any
           previously played pieces; and
         - the piece shares one or more corners but no edges
           with the player's previously played pieces.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """

        if piece.shape.kind not in self.remaining_shapes(self._curr_player):
            raise ValueError("The player has already played a piece with this shape.")

        if piece.anchor is None:
            raise ValueError("The anchor of the piece is None.")

        if self.any_collisions(piece):
            return False

        valid = False
        if self._num_moves < self.num_players - len(self.retired_players):
            for square in piece.squares():
                if square in self._start_positions:
                    valid = True
                    break
            return valid

        for r,c in piece.cardinal_neighbors():
            if r < self.size and r >= 0 and c < self.size and c >= 0:
                cell = self.grid[r][c]
                if cell != None:
                    if cell[0] == self.curr_player:
                        return False

        corner = False
        for r,c in piece.intercardinal_neighbors():
            if r < self.size and r >= 0 and c < self.size and c >= 0:
                cell = self.grid[r][c]
                if cell != None:
                    if cell[0] == self.curr_player:
                        corner = True
                        break
        return corner

    def maybe_place(self, piece: Piece) -> bool:
        """
        If the piece is legal to place, this method
        places the piece on the board, updates the
        current player and other relevant game state,
        and returns True.

        If not, this method leaves the board and current
        game state unmodified, and returns False.

        Note that the game does not necessarily end right
        away when a player places their last piece; players
        who have not retired and have remaining pieces
        should still get their turns.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        if self._curr_player in self._retired_players:
            return False

        if not self.legal_to_place(piece):
            return False

        if piece.shape.kind not in self.remaining_shapes(self._curr_player):
            raise ValueError

        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)

        self._played_pieces.append((self.curr_player, piece.shape.kind))

        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1

        if len(self._retired_players) != self._num_players:
            while self._curr_player in self.retired_players:
                self._curr_player = (self._curr_player % self.num_players) + 1
        else:
            self._curr_player = (self._curr_player % self.num_players) + 1

        return True

    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        if self._curr_player not in self.retired_players:
            self.retired_players.add(self._curr_player)

        if len(self._retired_players) != self._num_players:
            while self._curr_player in self.retired_players:
                self._curr_player = (self._curr_player % self.num_players) + 1
        else:
            self._curr_player = (self._curr_player % self.num_players) + 1


    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        score = 0
        pieces = self.remaining_shapes(player)
        if len(pieces) != 0:
            for piece in pieces:
                if piece in definitions: #test consolidation if this works
                    shape_definitions = definitions[piece].strip()
                    shape_definitions = shape_definitions.replace(" ", "")
                    shape_definitions = shape_definitions.replace("@", "")
                    shape_definitions = ''.join(shape_definitions.splitlines())
                    score -= len(shape_definitions)
        else:
            bonus = False
            for x in range (-1, -(len(self._played_pieces)), -1):
                played_piece = self._played_pieces[x]
                if played_piece[0] == player:
                    if played_piece[1] == ShapeKind.ONE:
                        score += 20
                        bonus = True
                        break
            if not bonus:
                score += 15

        return score

    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Notice there may be many different Pieces corresponding
        to a single Shape that are considered available moves
        (because they may differ in location and orientation).
        """
        possible_moves = set()
        remaining_shapes = self.remaining_shapes(self.curr_player)

        for r in range(self.size):
            for c in range(self.size):
                for shape_kind in remaining_shapes:
                    shape = self.shapes[shape_kind]
                    piece = Piece(shape)
                    piece.set_anchor((r, c))

                    if self.legal_to_place(piece):
                        possible_moves.add(piece)
        return possible_moves

    def reset(self):
        """
        Resets the game state to start a new game.
        """
        self._grid = [[None] * self._size for _ in range(self._size)]
        self._curr_player = 1
        self._num_moves = 0
        self._retired_players = set()