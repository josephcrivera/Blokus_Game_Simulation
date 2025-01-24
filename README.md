# CMSC 14200 Course Project

Team members:
- GUI: Chris Mesch (chrismesch)
- BOT: Gabriel Ramos (ramosg)
- QA: Dylan Wilson (dylanwilson)
- TUI: Joe Rivera (josephrivera)

GUI Instructions:

UP = Move Piece Up
DOWN = Move Piece Down
LEFT = Move Piece Left
RIGHT = Move Piece Right
E = Rotate Left
R = Rotate Right
SPACE = Flip Horizontally

Enter = Attempt to place piece
Q = Retire
ESC = Quit Window

Piece Selection = Key Corresponding to Available Pieces!

Documentation

Improvements:

Game Logic:

Code Completeness (N)
Grading comment:
Issue with Start Positions. See code comment(s)
[Code Correctness] This structure of your control flow
does not capture the case where: a player tries to play their first piece
somewhere such that none of it's squares cover a starting position

Improvements Made:
We had an issue where, while we were keeping track of start positions, our code
did not halt players from placing their first move anywhere on the board. Our
logic didn't force players to start on the start position.

So, for Milestone 3, we added a boolean switch to the "legal_to_place" method.
This allowed us to return "False" for legal to place, until the squares in
"Start Positions" were covered. Once they were, the boolean switches to "True"
and removes that constraint, allowing the players to continue placing other
legal moves.

This can be found in blokus.py / legal_to_place / Lines ~283 - 289

GUI:
Code Quality (N)
Grading Comment:
[Code Quality] Missing docstrings for new functions/methods

Improvements Made:
Because this comment was general across the gui.py file, I went ahead and
cleaned up the docstrings/documentation throughout the document. The file
should now have adequate docstring documentation so is easy to see which parts
of the code do what.

TUI:
Code Quality (N)
Grading Comment:
[Code Quality] Running python3 src/{g,t}ui.py 20 doesn’t correctly display the board, start positions, and initial randomly selected piece

Improvements Made:
This error resulted from a lack of starting positions in the displayed view. Now,  I made sure to initialize the respective starting positions based on the type of Blokus game being created. This method of running the file has changed to utilize the click library and terminal arguments but I kept the same principles in mind to address this issue. This can be seen in the "board_creation" function.

Bot: This componint received two S scores in Milestone 2.

QA: This component received two S scores in Milestone 2.
