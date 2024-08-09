from typing import List, Literal

from src.constants import CAPTURED_GOATS_TO_WIN, GOAT_PLAYER, TIGER_PLAYER
from src.game.game_types import BoardSquare, Capture, Play
from src.game.game_state import GameState
from src.game.board import Board


class Game:
    def __init__(self, board: Board = None, game_state: GameState = None):
        self.board: Board = board or Board()
        self.game_state: GameState = game_state or GameState()

    def ply(self, move: Play):
        """Make the move of a single player."""
        self.board.move(move)

        if isinstance(move, BoardSquare):
            self.game_state.positioned_goats += 1
        elif isinstance(move, Capture):
            self.game_state.captured_goats += 1

        if self.game_state.player == TIGER_PLAYER:
            self.game_state.player = GOAT_PLAYER
        else:
            self.game_state.player = TIGER_PLAYER

    def available_moves(self) -> List[Play]:
        """Return a list of the available moves."""
        return self.board.available_moves(self.game_state)

    def is_game_over(self) -> bool:
        """Return True if the game ended, False otherwise."""
        if self._captured_required_goats() or self._trapped_tigers():
            return True

        return False

    def get_winner(self) -> Literal[-1, 1] | None:
        """Return the winner of the game, or None if it's not over"""
        if self._captured_required_goats():
            return TIGER_PLAYER

        if self._trapped_tigers():
            return GOAT_PLAYER

        return None

    def _captured_required_goats(self) -> bool:
        if self.game_state.captured_goats >= CAPTURED_GOATS_TO_WIN:
            return True

        return False

    def _trapped_tigers(self) -> bool:
        if self.game_state.player == TIGER_PLAYER and len(self.board.available_moves(self.game_state)) == 0:
            return True

    def print_game_info(self):
        """Print the state of the game, including the state and the board."""
        print("-" * 80)
        print(f"Current player: {'Tiger' if self.game_state.player == TIGER_PLAYER else 'GOAT'}")
        print(
            f"Total Positioned Goats: {self.game_state.positioned_goats}"
            f"       ---       "
            f"Total captured goats: {self.game_state.captured_goats}"
        )
        print("-" * 80)
        self.board.print_board()
