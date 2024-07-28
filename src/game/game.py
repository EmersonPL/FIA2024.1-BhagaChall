from typing import List, Literal, Tuple

from src.constants import GOAT_PLAYER, TIGER_PLAYER
from src.game.game_types import Play
from src.game.game_state import GameState
from src.game.board import Board


class Game:
    def __init__(self, board: Board = None, game_state: GameState = None):
        self.board: Board = board or Board()
        self.game_state: GameState = game_state or GameState()

    def available_moves(self) -> List[Play]:
        """Return a list of the available moves."""
        return self.board.available_moves(self.game_state)

    def is_game_over(self) -> Tuple[bool, Literal[-1, 1] | None]:
        """Return a tuple indicating if the game is over and it's winner."""
        if self.game_state.captured_goats >= 5:
            return True, TIGER_PLAYER

        if self.game_state.player == TIGER_PLAYER and len(self.board.available_moves(self.game_state)) == 0:
            return True, GOAT_PLAYER

        return False, None
