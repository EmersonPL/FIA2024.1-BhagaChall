from typing import List, Literal

import numpy as np
import numpy.typing as npt

from src.constants import (
    BOARD_COLS,
    BOARD_LINES,
    GOAT_PLAYER,
    TIGER_PLAYER,
    TOTAL_NUMBER_OF_GOATS,
)
from src.game.game_types import BoardSquare, Capture, Movement, Play
from src.game.game_state import GameState
from src.game.board import Board


class Game:
    def __init__(self, board: Board = None, game_state: GameState = None):
        self.board: Board = board or Board()
        self.game_state: GameState = game_state or GameState()

    def available_moves(self) -> List[Play]:
        """Return a list of the available moves."""
        return self.board.available_moves(self.game_state)
