from typing import List, Literal

import numpy as np
import numpy.typing as npt

from src.constants import (
    BOARD_COLS,
    BOARD_LINES,
    CLEAN_SQUARE,
    GOAT_PLAYER,
    TIGER_PLAYER,
    TOTAL_NUMBER_OF_GOATS,
)
from src.game.game_state import GameState
from src.game.game_types import BoardSquare, Capture, Movement, Play
from src.utils import neighboring_squares


class Board:
    def __init__(self, board: npt.NDArray = None):
        self.board: npt.NDArray = board
        if self.board is None:
            self._setup_initial_board()

    def _setup_initial_board(self):
        board = np.zeros([BOARD_LINES, BOARD_COLS], dtype=int)
        board[0, 0] = TIGER_PLAYER
        board[0, BOARD_COLS - 1] = TIGER_PLAYER
        board[BOARD_LINES - 1, 0] = TIGER_PLAYER
        board[BOARD_LINES - 1, BOARD_COLS - 1] = TIGER_PLAYER

        self.board = board

    def move(self, move: Play):
        """Make a move in the board.

        The move can be a placement of a goat, a movement of a tiger or goat, or the capture of a goat by a tiger.
        """
        if isinstance(move, BoardSquare):
            self.board[move.lin, move.col] = GOAT_PLAYER

        elif isinstance(move, Movement):
            initial_piece = self.board[move.start.lin, move.start.col]
            self.board[move.end.lin, move.end.col] = initial_piece

            self.board[move.start.lin, move.start.col] = CLEAN_SQUARE

        elif isinstance(move, Capture):
            self.board[move.starting_square.lin, move.starting_square.col] = (
                CLEAN_SQUARE
            )
            self.board[move.captured.lin, move.captured.col] = CLEAN_SQUARE
            self.board[move.ending_square.lin, move.ending_square.col] = (
                TIGER_PLAYER
            )

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
        return self._get_piece_positions(CLEAN_SQUARE)

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

    def _get_piece_positions(
        self, piece_type: Literal[-1, 0, 1]
    ) -> List[BoardSquare]:
        lines, cols = np.where(self.board == piece_type)
        pos = [
            BoardSquare(lin=int(line), col=int(col))
            for line, col in zip(lines, cols)
        ]
        return pos

    def _get_piece_movements(self, piece_pos: BoardSquare) -> List[Movement]:
        moves = neighboring_squares(piece_pos)

        allowed_moves = [
            Movement(piece_pos, move)
            for move in moves
            if self.board[move.lin, move.col] == 0
        ]
        return allowed_moves

    def _get_piece_capture_moves(self, piece_pos: BoardSquare) -> List[Capture]:
        neighbors = neighboring_squares(piece_pos)

        capture_movements = []
        for neighbor_pos in neighbors:
            square_after_capture = self._get_square_after_capture(
                piece_pos, neighbor_pos
            )
            if square_after_capture:
                capture_movements.append(
                    Capture(
                        starting_square=piece_pos,
                        ending_square=square_after_capture,
                        captured=neighbor_pos,
                    )
                )

        return capture_movements

    def _get_square_after_capture(
        self, tiger_pos: BoardSquare, goat_pos: BoardSquare
    ) -> BoardSquare | None:
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
        if (
            piece_in_new_square == TIGER_PLAYER
            or piece_in_new_square == GOAT_PLAYER
        ):
            return None

        return BoardSquare(new_lin, new_col)

    def count_number_of_locked_tigers(self):
        """Return the number of locked tigers."""
        locked_tigers = 0
        for tiger in self._get_piece_positions(TIGER_PLAYER):
            moves = []
            moves.extend(self._get_piece_movements(tiger))
            moves.extend(self._get_piece_capture_moves(tiger))

            if len(moves) == 0:
                locked_tigers += 1

        return locked_tigers

    def __str__(self):
        board = ""

        for lin in self.board:
            for col in lin:
                board += str(col)

        return board

    def print_board(self):
        board_str = (
            "P---P---P---P---P\n"
            "|\\  |  /|\\  |  /|\n"
            "| \\ | / | \\ | / |\n"
            "|  \\|/  |  \\|/  |\n"
            "P---P---P---P---P\n"
            "|  /|\\  |  /|\\  |\n"
            "| / | \\ | / | \\ |\n"
            "|/  |  \\|/  |  \\|\n"
            "P---P---P---P---P\n"
            "|\\  |  /|\\  |  /|\n"
            "| \\ | / | \\ | / |\n"
            "|  \\|/  |  \\|/  |\n"
            "P---P---P---P---P\n"
            "|  /|\\  |  /|\\  |\n"
            "| / | \\ | / | \\ |\n"
            "|/  |  \\|/  |  \\|\n"
            "P---P---P---P---P\n"
        )

        intersect_count = 0
        for i, char in enumerate(board_str):
            if char == "P":
                piece = self.board[
                    intersect_count // BOARD_LINES, intersect_count % BOARD_COLS
                ]
                if piece == GOAT_PLAYER:
                    piece_str = "G"
                elif piece == TIGER_PLAYER:
                    piece_str = "T"
                else:
                    piece_str = "O"

                pre_str = board_str[:i]
                post_str = board_str[i + 1 :]
                board_str = pre_str + piece_str + post_str
                intersect_count += 1

        print(board_str)
