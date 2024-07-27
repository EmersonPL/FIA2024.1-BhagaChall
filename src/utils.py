from typing import List

from src.constants import AVAILABLE_DIAGONAL_MOVEMENTS, BOARD_COLS, BOARD_LINES
from src.game.game_types import BoardSquare


def neighboring_squares(piece_pos: BoardSquare) -> List[BoardSquare]:
    """Return all neighbor squares of `piece_pos`."""
    lin, col = piece_pos.lin, piece_pos.col

    moves = []
    if lin > 0:
        moves.append(BoardSquare(lin - 1, col))
    if lin < BOARD_LINES - 1:
        moves.append(BoardSquare(lin + 1, col))
    if col > 0:
        moves.append(BoardSquare(lin, col - 1))
    if col < BOARD_COLS - 1:
        moves.append(BoardSquare(lin, col + 1))

    moves.extend(list_of_available_diagonal_movements(piece_pos))
    return moves


def list_of_available_diagonal_movements(pos: BoardSquare) -> List[BoardSquare]:
    """Return the list of available diagonal movements from a square"""
    try:
        return AVAILABLE_DIAGONAL_MOVEMENTS[pos]
    except KeyError:
        return []
