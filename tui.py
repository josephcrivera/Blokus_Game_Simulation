"""
TUI for Blokus Project for CS 142
"""
from typing import Any
import curses
import random
import sys
import click
from blokus import Blokus
from piece import Piece, ShapeKind, copy, Point

ENTER_KEYS = [10, 13]
ESC = 27
R_KEY = 114
E_KEY = 101
Q_KEY = 113
SPACE = 32

class TuiBoard:
    """
    A Blokus game that allows the user to play
    """
    def __init__(self, screen: Any, size: int, num_players: int, start_positions: set[Point]):
        """
        Constructor that initializes the game and then starts playing it
        """
        self.game = Blokus(num_players, size, start_positions)

        try:
            self.screen = screen # initialize screen
            curses.noecho()
            curses.cbreak()
            curses.set_escdelay(25)
            self.colors() #initialize custom colors
            self.play() #start game here
        except Exception:
            self.end_tui()
            raise
        self.end_tui()

    def colors(self) -> None:
        """
        Create a custom set of colors and initialize those colors for specific
        numbers
        """
        curses.start_color()
        curses.init_color(1, 1000, 0, 0)#red for player 1
        curses.init_color(2, 0, 0, 1000) #blue for player 2
        curses.init_color(3, 1000, 647, 0)#orange for player 3
        curses.init_color(4, 1000, 0, 498)#pink for player 4
        curses.init_color(5, 1000, 1000, 0) #yellow for starting pos
        curses.init_color(6, 0, 1000, 0) #green for pending pieces/current player
        curses.init_color(7, 501, 501, 501) #grey for border
        curses.init_color(8, 1000, 1000, 1000) #white for empty

        curses.init_pair(1, 1, curses.COLOR_BLACK)
        curses.init_pair(2, 2, curses.COLOR_BLACK)
        curses.init_pair(3, 3, curses.COLOR_BLACK)
        curses.init_pair(4, 4, curses.COLOR_BLACK)
        curses.init_pair(5, 5, curses.COLOR_BLACK)
        curses.init_pair(6, 6, curses.COLOR_BLACK)
        curses.init_pair(7, 7, curses.COLOR_BLACK)
        curses.init_pair(8, 8, curses.COLOR_BLACK)

    def border(self, border_size: int, cell: str) -> None:
        """
        Simple function to output the border cells onto the screen
        """
        for _ in range(border_size):
            self.screen.addstr(cell + " ", curses.color_pair(7))#grey border
        self.screen.addstr("\n")

    def update_board(self, piece: Piece | None = None) -> None:
        """
        Display the board with all of the pieces in their repsective colors. If 
        there is a pending piece, display that in green.
        """
        border_size = self.game.size + 2
        cell = "\u2584" # Unicode character for a box
        self.screen.addstr("*** Blokus Movement Board ***\n")
        self.screen.addstr(f"Current Player: {self.game.curr_player}\n")

        self.border(border_size, cell)

        for i, row in enumerate(self.game.grid):
            self.screen.addstr(cell + " ", curses.color_pair(7))#grey border
            for j, col in enumerate(row):

                if piece is not None and (i, j) in piece.shape.squares:
                    self.screen.addstr(cell + " ", curses.color_pair(6)) #green pending
                elif col is None:
                    if (i,j) in self.game.start_positions:
                        self.screen.addstr(cell + " ", curses.color_pair(5))#yellow start position
                    else:
                        self.screen.addstr(cell + " ", curses.color_pair(8))#white empty
                elif col is not None:
                    player = col[0]
                    self.screen.addstr(cell + " ", curses.color_pair(player))#player color
            self.screen.addstr(cell + " \n", curses.color_pair(7))#border grey

        self.border(border_size, cell)

    def update_status(self) -> None:
        """
        Display the Player's number and the shapes that they have left as well
        as if they are retired and their current score
        """
        for player in range(1, self.game.num_players+1):
            left = self.game.shapes

            if player == self.game.curr_player:
                self.screen.addstr(f"Player {player}: ", curses.color_pair(6))# green current player
            else:
                self.screen.addstr(f"Player {player}: ", curses.color_pair(7))#grey
            for shape in left:
                if shape in self.game.remaining_shapes(player):
                    self.screen.addstr(shape.value + " ", curses.color_pair(player)) #player color
                else:
                    self.screen.addstr(shape.value + " ", curses.color_pair(7))#grey
            self.screen.addstr(f"| Current Score: {self.game.get_score(player)}")
            self.screen.addstr(f" | Retired?: {player in self.game.retired_players}")
            self.screen.addstr("\n")

    def end_screen(self) -> None:
        """
        Wipe the current display and present an ending screen with the winner(s)
        and their respective score(s)
        """
        self.screen.clear()
        winners = self.game.winners
        assert winners is not None
        high_score = self.game.get_score(winners[0])

        if len(winners) > 1:
            self.screen.addstr("Players ")
            for x in winners:
                if x == winners[-1]:
                    self.screen.addstr(f"and {x} ")
                else:
                    self.screen.addstr(f"{x}, ")
            self.screen.addstr(f"have tied the game with a score of {high_score}.\n")
        else:
            self.screen.addstr(f"Player {winners[0]} won with a score of {high_score}.\n")
        self.screen.addstr("Press any key to exit the game\n")
        _ = self.screen.getkey()

    def play(self) -> None:
        """
        Display the board with everyone's pieces and a desciption of the 
        statuses of each player. Allow the player to choose a piece to play or
        to retire
        """
        end = False
        while not end:
            valid = False
            r_selected = random.choice(self.game.remaining_shapes(self.game.curr_player))
            rando_p = self.center_piece(r_selected)

            while not valid:
                self.update_board(rando_p)
                self.update_status()
                self.screen.addstr("\nThe current pending piece is highlighted in green.")
                self.screen.addstr("\nTo play the current piece or to change it, hit the corresponding key. [Q to Retire]\n")
                pick = self.screen.getch()
                pending: ShapeKind

                if pick == ESC:
                    sys.exit(0)
                elif pick == Q_KEY:
                    valid = True
                    self.game.retire()
                else:
                    for shape in self.game.remaining_shapes(self.game.curr_player):
                        if shape.value.lower() == chr(pick):
                            pending = shape
                            valid = True
                            break
                    if valid:
                        self.move_pieces(pending)
                self.screen.clear()
            end = self.game.game_over
        self.end_screen()

    def center_piece(self, sk: ShapeKind) -> Piece:
        """
        Method to create and place pieces in the center of the board
        """
        piece = Piece(self.game.shapes[sk])
        piece.shape.origin = (0, 0)
        piece.set_anchor(piece.shape.origin)

        if piece.shape.kind == ShapeKind.V:
            piece.shape.origin = piece.shape.squares[-1]

        new_x, new_y = ((self.game.size // 2), (self.game.size // 2))

        piece = self.shift(piece, new_y, new_x)

        if piece.shape.kind == ShapeKind.V:
            self.shift(piece, -1, -1)
        return piece

    def move_pieces(self, block: ShapeKind) -> None:
        """
        Display a board for moving the pieces and the instructions for the user.
        Allow them to keep moving the piece until they place it or retire
        """
        piece = self.center_piece(block)

        done = False
        while not done:
            self.screen.clear()
            self.update_board(piece)
            self.screen.addstr(f"Pending Piece: {piece.shape.kind.value}\n")
            self.screen.addstr("\nMove the piece using the arrow keys.\n")
            self.screen.addstr("Rotate the piece using the E (left) and R (right).\nFlip the piece horizontally with the spacebar.\n")
            self.screen.addstr("Retire with Q or use the ENTER key when you are ready to place.\n")
            first_char = self.screen.getch()
            if first_char == ESC: # ESC key
                sys.exit(0)
            elif first_char in ENTER_KEYS: # RETURN/ENTER key
                if self.game.maybe_place(piece):
                    done = True
                else:
                    continue
            elif first_char == Q_KEY:
                self.game.retire()
                done = True
            else:
                holder = None
                if first_char == curses.KEY_UP:
                    holder = self.shift(piece, 0, -1)
                elif first_char == curses.KEY_RIGHT:
                    holder = self.shift(piece, 1, 0)
                elif first_char == curses.KEY_LEFT:
                    holder = self.shift(piece, -1, 0)
                elif first_char == curses.KEY_DOWN:
                    holder = self.shift(piece, 0, 1)
                elif first_char == R_KEY:
                    holder = self.rotate(piece, "R")
                elif first_char == E_KEY:
                    holder = self.rotate(piece, "L")
                elif first_char == SPACE:
                    holder = self.flip(piece)
                else:
                    self.screen.addstr("Please use the proper keys")
                    continue

                if holder is not None:
                    piece = holder

    def shift(self, piece: Piece, new_y: int, new_x: int) -> Piece:
        """
        Shift the piece in any direction and return it unless there will be a 
        wall collision. If so, return the original state of the piece. 
        """
        prev_state = copy.deepcopy(piece)
        old_x, old_y = piece.shape.origin

        x_diff = old_x + new_x
        y_diff = old_y + new_y

        new_sqs = []
        for x,y in piece.shape.squares:
            if (x,y) == piece.shape.origin:
                piece.shape.origin = (x_diff, y_diff)
            new_sqs.append((x + new_x, y + new_y))
        piece.shape.squares = new_sqs
        if self.game.any_wall_collisions(piece):
            return prev_state
        return piece

    def rotate(self, piece: Piece, direction: str) -> Piece:
        """
        Rotate the piece right or left and return it unless there will be a wall 
        collision. If so, return the original state of the piece. 
        """
        prev_state = copy.deepcopy(piece)
        old_x, old_y = piece.shape.origin

        if direction == "R":
            piece.rotate_right()
            piece.shape.origin = (piece.shape.origin[1], -piece.shape.origin[0])
        elif direction == "L":
            piece.rotate_left()
            piece.shape.origin = (-piece.shape.origin[1], piece.shape.origin[0])

        new_x, new_y = piece.shape.origin
        x_diff = old_x - new_x
        y_diff = old_y - new_y
        new_sqs = []
        for x,y in piece.shape.squares:
            if (x,y) == piece.shape.origin:
                x += x_diff
                y += y_diff
                piece.shape.origin = (x, y)
            else:
                x += x_diff
                y += y_diff
            new_sqs.append((x, y))
        piece.shape.squares = new_sqs
        if self.game.any_wall_collisions(piece):
            return prev_state
        return piece

    def flip(self, piece: Piece) -> Piece:
        """
        Flip the piece horizontally and return it unless there will be a wall 
        collision. If so, return the original state of the piece. 
        """
        prev_state = copy.deepcopy(piece)
        old_y = piece.shape.origin[1]
        piece.flip_horizontally()
        piece.shape.origin = (piece.shape.origin[0], -piece.shape.origin[1])
        new_y = piece.shape.origin[1]
        new_sqs = []
        diff = old_y - new_y
        for x,y in piece.shape.squares:
            if (x,y) == piece.shape.origin:
                y = y + diff
                piece.shape.origin = (x, y)
            else:
                y = y + diff
            new_sqs.append((x, y))
        piece.shape.squares = new_sqs
        if self.game.any_wall_collisions(piece):
            return prev_state
        return piece

    def end_tui(self) -> None:
        """
        End the curses screen
        """
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()


def start(screen: Any, size: int, num_player: int, start_positions: set[Point]) -> None:
    """
    Create the Blokus board and start playing the game
    """
    TuiBoard(screen, size, num_player, start_positions)

@click.command()
@click.option('-s', '--size', default = 14, type = int, help = 'Size of the Blokus Board')
@click.option('-n', '--num_players', default = 2, type = int, help = 'Number of players')
@click.option('-p', '--start_position', default = ((4,4), (9,9)), multiple = True, nargs =2, type = int, help = 'Starting positions')
@click.option('--game', type = click.Choice(['mono', 'duo', 'classic-2', 'classic-3', 'classic-4'], case_sensitive = False))
def board_creation(size: int, num_players: int, start_position: set[Point], game: str) -> None:
    """
    Gather information about the type of Blokus game from the terminal and send 
    it to the be processed into a Blokus game object
    """
    if game is not None:
        if game == "mono":
            size = 11
            num_players = 1
            start_position = {(5,5)}
        elif game == "duo":
            size = 14
            num_players = 2
            start_position = {(4,4), (9,9)}
        else:
            size = 20
            start_position = {(0,0), (0,19), (19,0), (19,19)}
            if game == "classic-2":
                num_players = 2
            elif game == "classic-3":
                num_players = 3
            elif game == "classic-4":
                num_players = 4
    curses.wrapper(start, size, num_players, start_position)

if __name__ == "__main__":
    board_creation()
