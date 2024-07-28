from typing import List, Literal

import numpy as np
import numpy.typing as npt

from src.constants import BOARD_COLS, BOARD_LINES, GOAT_PLAYER, TIGER_PLAYER, TOTAL_NUMBER_OF_GOATS
from src.game.game_state import GameState
from src.game.game_types import BoardSquare, Capture, Movement, Play
from src.utils import neighboring_squares


class Board:
    def __init__(self, board: npt.NDArray = None):
        self.board: npt.NDArray = board
        if self.board is None:
            self._setup_initial_board()

    def _setup_initial_board(self):
        board = np.zeros([BOARD_LINES, BOARD_COLS])
        board[0, 0] = TIGER_PLAYER
        board[0, BOARD_COLS - 1] = TIGER_PLAYER
        board[BOARD_LINES - 1, 0] = TIGER_PLAYER
        board[BOARD_LINES - 1, BOARD_COLS - 1] = TIGER_PLAYER

        self.board = board

    def available_moves(self, game_state: GameState) -> List[Play]:
        """Return a list of the available moves for the given game state."""
        if game_state.player == GOAT_PLAYER:
            return self._goat_movements(game_state.positioned_goats)

        return self._tiger_movements()

    def _goat_movements(self, positioned_goats: int) -> List[Play]:
        if positioned_goats < TOTAL_NUMBER_OF_GOATS:
            return self._goat_placement_moves()

        moves = []
        for goat in self._get_piece_positions(GOAT_PLAYER):
            moves.extend(self._get_piece_movements(goat))

        return moves

    def _goat_placement_moves(self) -> List[BoardSquare]:
        """Return all empty board squares."""
        return self._get_piece_positions(0)

    def _tiger_movements(self) -> List[Movement | Capture]:
        normal_moves = []
        capture_moves = []

        for tiger in self._get_piece_positions(TIGER_PLAYER):
            normal_moves.extend(self._get_piece_movements(tiger))
            capture_moves.extend(self._get_piece_capture_moves(tiger))

        if capture_moves:
            # Force the selection of a capture, if any is available
            return capture_moves

        return normal_moves

    def _get_piece_positions(self, piece_type: Literal[-1, 0, 1]) -> List[BoardSquare]:
        lines, cols = np.where(self.board == piece_type)
        pos = [BoardSquare(lin=int(line), col=int(col)) for line, col in zip(lines, cols)]
        return pos

    def _get_piece_movements(self, piece_pos: BoardSquare) -> List[Movement]:
        moves = neighboring_squares(piece_pos)

        allowed_moves = [Movement(piece_pos, move) for move in moves if self.board[move.lin, move.col] == 0]
        return allowed_moves

    def _get_piece_capture_moves(self, piece_pos: BoardSquare) -> List[Capture]:
        neighbors = neighboring_squares(piece_pos)

        capture_movements = []
        for neighbor_pos in neighbors:
            square_after_capture = self._get_square_after_capture(piece_pos, neighbor_pos)
            if square_after_capture:
                capture_movements.append(
                    Capture(starting_square=piece_pos, ending_square=square_after_capture, captured=neighbor_pos)
                )

        return capture_movements

    def _get_square_after_capture(self, tiger_pos: BoardSquare, goat_pos: BoardSquare) -> BoardSquare | None:
        """Return the square where the piece will be after capturing, or None if the capture is not allowed."""
        if self.board[goat_pos.lin, goat_pos.col] != GOAT_PLAYER:
            return None

        tiger_lin, tiger_col = tiger_pos.lin, tiger_pos.col
        goat_lin, goat_col = goat_pos.lin, goat_pos.col

        new_lin = goat_lin + (goat_lin - tiger_lin)
        new_col = goat_col + (goat_col - tiger_col)

        if new_lin >= BOARD_LINES or new_col >= BOARD_COLS:
            return None

        if new_lin < 0 or new_col < 0:
            return None

        piece_in_new_square = self.board[new_lin, new_col]
        if piece_in_new_square == TIGER_PLAYER or piece_in_new_square == GOAT_PLAYER:
            return None

        return BoardSquare(new_lin, new_col)
