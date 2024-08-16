from math import inf

from constants import TIGER_PLAYER
from game.game import Game
from game.game_types import Capture


def dummy_heuristic_goat(game: Game) -> int | float:
    return +inf


def dummy_heuristic_tiger(game: Game) -> int | float:
    return -inf


def heuristic(game: Game) -> int | float:
    num_goat = game.game_state.positioned_goats - game.game_state.captured_goats
    locked_tigers = game.count_number_of_locked_tigers() * 50

    value_captured_goat = 10 * game.game_state.captured_goats
    tiger_moves = _calculate_tiger_moves_score(game)

    game_board_value = (
        num_goat + locked_tigers - value_captured_goat - tiger_moves
    )

    return game_board_value


def _calculate_tiger_moves_score(game: Game) -> int:
    current_player = game.game_state.player
    game.game_state.player = TIGER_PLAYER

    score = 0
    allowed_moves = game.available_moves()
    for move in allowed_moves:
        if isinstance(move, Capture):
            score += 50
        else:
            score += 5

    game.game_state.player = current_player
    return score
