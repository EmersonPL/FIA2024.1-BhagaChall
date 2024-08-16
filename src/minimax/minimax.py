from collections import deque
from math import inf
from typing import Callable, Tuple

from constants import GOAT_PLAYER
from minimax.search_tree import SearchTree
from game.game import Game


def alpha_beta_search(
    game: Game = None,
    move: Tuple[int, int] | None = None,
    node: SearchTree = None,
    cutoff: int = None,
    heuristic: Callable[[Game], int] = None,
) -> SearchTree:
    if not game:
        game = Game()
    if not node:
        node = SearchTree(game, move)
        node.value = -inf if node.game.game_state.player == GOAT_PLAYER else inf

    if cutoff is not None and node.depth > cutoff:
        winner = game.get_winner()
        if winner is not None:
            node.value = winner * inf
        elif heuristic is not None:
            node.value = heuristic(game)

        return node

    node.expand_children()

    if game.game_state.player == GOAT_PLAYER:
        for curr_node in node.children:
            if curr_node.value is None:
                curr_node.value = inf

            n = alpha_beta_search(
                curr_node.game, curr_node.move, curr_node, cutoff, heuristic
            )

            if n.value > node.value:
                node.value = n.value
                node.alpha = max(node.alpha, n.value)
            if node.parent and node.value >= node.parent.beta:
                return node

    else:
        for curr_node in node.children:
            if curr_node.value is None:
                curr_node.value = -inf

            n = alpha_beta_search(
                curr_node.game, curr_node.move, curr_node, cutoff, heuristic
            )

            if n.value < node.value:
                node.value = n.value
                node.beta = min(node.beta, n.value)
            if node.parent and node.value <= node.parent.alpha:
                return node

    return node


def minimax(game: Game = None, move: Tuple[int, int] | None = None, **kwargs):
    """Return a search tree with the result for perfect play in each node."""
    if not game:
        game = Game()

    node = SearchTree(game, move)

    frontier = deque([node])

    while frontier:
        curr_node = frontier.pop()
        curr_node.expand_children()

        for child in curr_node.children:
            frontier.append(child)

    node.update_value()

    return node
