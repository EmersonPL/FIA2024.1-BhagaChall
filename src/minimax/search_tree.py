from copy import deepcopy
from math import inf
from typing import List, Tuple

from constants import GOAT_PLAYER
from game.game import Game


class SearchTree:
    """Class to implement a tree-based search for the minmax algorithm."""

    def __init__(
        self,
        game: Game,
        move: Tuple[int, int] | None,
        parent=None,
        depth: int = 0,
    ):
        self.game = game
        self.move = move
        self.children: List[SearchTree] = []
        self.parent = parent
        self.alpha = -inf
        self.beta = inf
        self.depth = depth

        winner = self.game.get_winner()

        self.end = winner is not None

        if winner is None:
            self.value = None
        else:
            self.value = winner * inf

    def expand_children(self):
        if self.end:
            return

        for movement in self.game.available_moves():
            new_game = deepcopy(self.game)
            new_game.ply(movement)
            self.children.append(SearchTree(new_game, movement, self, depth=self.depth + 1))

    def update_value(self):
        """Update the values of all nodes in the tree"""
        if self.value is not None:
            # Already updated value, must be a final state
            return

        for child in self.children:
            child.update_value()

        values = [child.value for child in self.children]
        if self.game.game_state.player == GOAT_PLAYER:
            self.value = max(values)
        else:
            self.value = min(values)
