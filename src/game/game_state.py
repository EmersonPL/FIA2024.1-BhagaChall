from dataclasses import dataclass

from src.constants import GOAT_PLAYER


@dataclass
class GameState:
    """Current state of the game."""

    player: int = GOAT_PLAYER
    positioned_goats: int = 0
    captured_goats: int = 0
