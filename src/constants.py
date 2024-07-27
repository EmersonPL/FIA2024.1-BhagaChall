"""Constants"""

from typing import Final, List

from src.utils import BoardSquare

BOARD_LINES: Final = 5
BOARD_COLS: Final = 5

TIGER_PLAYER: Final = -1
GOAT_PLAYER: Final = 1

# The "lines" of the board, in which the pieces can move
AVAILABLE_DIAGONAL_MOVEMENTS: Final = {
    # L0
    (0, 0): [(1, 1)],
    (0, 2): [(1, 1), (1, 3)],
    (0, 4): [(1, 3)],
    # L1
    (1, 1): [(0, 0), (0, 2), (2, 0), (2, 2)],
    (1, 3): [(0, 2), (0, 4), (2, 2), (2, 4)],
    # L2
    (2, 0): [(1, 1), (3, 1)],
    (2, 2): [(1, 1), (1, 3), (3, 1), (3, 3)],
    (2, 4): [(1, 3), (3, 3)],
    # L3
    (3, 1): [(2, 0), (2, 2), (4, 0), (4, 2)],
    (3, 3): [(2, 2), (2, 4), (4, 2), (4, 4)],
    # L4
    (4, 0): [(3, 1)],
    (4, 2): [(3, 1), (3, 3)],
    (4, 4): [(3, 3)],
}


def list_of_available_diagonal_movements(pos: BoardSquare) -> List[BoardSquare]:
    """Return the list of available diagonal movements from a square"""
    try:
        return AVAILABLE_DIAGONAL_MOVEMENTS[pos]
    except KeyError:
        return []
