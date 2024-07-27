from typing import List, Literal

import numpy as np
import numpy.typing as npt

from src.constants import (
    BOARD_COLS,
    BOARD_LINES,
    GOAT_PLAYER,
    TIGER_PLAYER,
    TOTAL_NUMBER_OF_GOATS,
    list_of_available_diagonal_movements,
)
from src.utils import BoardSquare, Movement, Play
from src.game.game_state import GameState


class Game:
    def __init__(self, board: npt.NDArray = None, game_state: GameState = None):
        self.board: npt.NDArray = board
        if self.board is None:
            self._setup_initial_board()
        self.game_state = game_state or GameState()

    def _setup_initial_board(self):
        board = np.zeros([BOARD_LINES, BOARD_COLS])
        board[0, 0] = TIGER_PLAYER
        board[0, BOARD_COLS - 1] = TIGER_PLAYER
        board[BOARD_LINES - 1, 0] = TIGER_PLAYER
        board[BOARD_LINES - 1, BOARD_COLS - 1] = TIGER_PLAYER

        self.board = board

    def available_moves(self) -> List[Play]:
        """Return a list of the available moves.

        The moves are a tuple of board squares, with the first one being the origin square (where the piece is),
        and the second is the target square.
        """
        if self.game_state.player == GOAT_PLAYER:
            return self._goat_movements()

        return self._tiger_movements()

    def _goat_movements(self) -> List[Play]:
        if self.game_state.positioned_goats < TOTAL_NUMBER_OF_GOATS:
            return self._goat_placement_moves()

        moves = []
        for goat in self._get_piece_positions(GOAT_PLAYER):
            moves.extend(self._get_piece_movements(goat))

        return moves

    def _goat_placement_moves(self) -> List[BoardSquare]:
        """Return all empty board squares."""
        return self._get_piece_positions(0)

    def _tiger_movements(self) -> List[Movement]:
        moves = []

        for tiger in self._get_piece_positions(TIGER_PLAYER):
            moves.extend(self._get_piece_movements(tiger))
            moves.extend(self._get_piece_capture_moves(tiger))

        return moves

    def _get_piece_positions(self, piece_type: Literal[-1, 0, 1]) -> List[BoardSquare]:
        lines, cols = np.where(self.board == piece_type)
        pos = [(int(line), int(col)) for line, col in zip(lines, cols)]
        return pos

    def _get_piece_movements(self, piece_pos: BoardSquare) -> List[Movement]:
        lin, col = piece_pos

        moves = []
        if lin > 0:
            moves.append((lin - 1, col))
        if lin < BOARD_LINES - 1:
            moves.append((lin + 1, col))
        if col > 0:
            moves.append((lin, col - 1))
        if col < BOARD_COLS - 1:
            moves.append((lin, col + 1))

        moves.extend(list_of_available_diagonal_movements(piece_pos))

        allowed_moves = [(piece_pos, move) for move in moves if self.board[move] == 0]
        return allowed_moves

    def _get_piece_capture_moves(self, piece_pos: BoardSquare) -> List[Movement]:
        return []
