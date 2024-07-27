from unittest import TestCase

import numpy as np

from src.constants import GOAT_PLAYER, TIGER_PLAYER
from src.game.game import Game


class TestAllowedTigerMovements(TestCase):
    def test_base_board_movements(self):
        expected = [
            ((0, 0), (0, 1)),
            ((0, 0), (1, 0)),
            ((0, 0), (1, 1)),
            ((0, 4), (0, 3)),
            ((0, 4), (1, 4)),
            ((0, 4), (1, 3)),
            ((4, 0), (3, 0)),
            ((4, 0), (4, 1)),
            ((4, 0), (3, 1)),
            ((4, 4), (4, 3)),
            ((4, 4), (3, 4)),
            ((4, 4), (3, 3)),
        ]

        game = Game()
        game.game_state.player = TIGER_PLAYER

        self.assertCountEqual(game.get_available_moves(), expected)

    def test_non_empty_board_movements(self):
        expected = [
            # T1
            ((0, 0), (0, 1)),
            ((0, 0), (1, 0)),
            # T2
            ((1, 1), (0, 1)),
            ((1, 1), (0, 2)),
            ((1, 1), (1, 0)),
            ((1, 1), (1, 2)),
            ((1, 1), (2, 0)),
            ((1, 1), (2, 1)),
            ((1, 1), (2, 2)),
            # T3
            ((4, 0), (3, 0)),
            ((4, 0), (3, 1)),
            # T4
            ((4, 1), (3, 1)),
            ((4, 1), (4, 2)),
        ]

        game = Game()
        game.game_state.player = TIGER_PLAYER
        game.board[0, 4] = 0
        game.board[1, 1] = TIGER_PLAYER
        game.board[4, 4] = 0
        game.board[4, 1] = TIGER_PLAYER

        self.assertCountEqual(game.get_available_moves(), expected)


class TestAllowedGoatMovements(TestCase):
    def test_base_board_movements(self):
        goats_positions = [(0, 1), (0, 2), (2, 2), (3, 3)]

        expected = [
            # G1
            ((0, 1), (1, 1)),
            # G2
            ((0, 2), (0, 3)),
            ((0, 2), (1, 1)),
            ((0, 2), (1, 2)),
            ((0, 2), (1, 3)),
            # G3
            ((2, 2), (1, 1)),
            ((2, 2), (1, 2)),
            ((2, 2), (1, 3)),
            ((2, 2), (2, 1)),
            ((2, 2), (2, 3)),
            ((2, 2), (3, 1)),
            ((2, 2), (3, 2)),
            # G4
            ((3, 3), (2, 3)),
            ((3, 3), (2, 4)),
            ((3, 3), (3, 2)),
            ((3, 3), (3, 4)),
            ((3, 3), (4, 2)),
            ((3, 3), (4, 3)),
        ]

        game = Game()
        for goat in goats_positions:
            game.board[goat] = GOAT_PLAYER

        self.assertCountEqual(game.get_available_moves(), expected)
