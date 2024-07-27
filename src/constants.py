"""Constants"""

from typing import Final

from src.game.game_types import BoardSquare

# Board configuration
BOARD_LINES: Final = 5
BOARD_COLS: Final = 5

# Game configuration
TOTAL_NUMBER_OF_GOATS: Final = 20
CAPTURED_GOATS_TO_WIN: Final = 5

TIGER_PLAYER: Final = -1
GOAT_PLAYER: Final = 1

# The "lines" of the board, in which the pieces can move
AVAILABLE_DIAGONAL_MOVEMENTS: Final = {
    # L0
    BoardSquare(0, 0): [BoardSquare(1, 1)],
    BoardSquare(0, 2): [BoardSquare(1, 1), BoardSquare(1, 3)],
    BoardSquare(0, 4): [BoardSquare(1, 3)],
    # L1
    BoardSquare(1, 1): [BoardSquare(0, 0), BoardSquare(0, 2), BoardSquare(2, 0), BoardSquare(2, 2)],
    BoardSquare(1, 3): [BoardSquare(0, 2), BoardSquare(0, 4), BoardSquare(2, 2), BoardSquare(2, 4)],
    # L2
    BoardSquare(2, 0): [BoardSquare(1, 1), BoardSquare(3, 1)],
    BoardSquare(2, 2): [BoardSquare(1, 1), BoardSquare(1, 3), BoardSquare(3, 1), BoardSquare(3, 3)],
    BoardSquare(2, 4): [BoardSquare(1, 3), BoardSquare(3, 3)],
    # L3
    BoardSquare(3, 1): [BoardSquare(2, 0), BoardSquare(2, 2), BoardSquare(4, 0), BoardSquare(4, 2)],
    BoardSquare(3, 3): [BoardSquare(2, 2), BoardSquare(2, 4), BoardSquare(4, 2), BoardSquare(4, 4)],
    # L4
    BoardSquare(4, 0): [BoardSquare(3, 1)],
    BoardSquare(4, 2): [BoardSquare(3, 1), BoardSquare(3, 3)],
    BoardSquare(4, 4): [BoardSquare(3, 3)],
}
