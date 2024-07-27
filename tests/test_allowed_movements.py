from unittest import TestCase

import numpy as np

from src.constants import GOAT_PLAYER, TIGER_PLAYER, TOTAL_NUMBER_OF_GOATS
from src.game.game import Game
from src.game.game_types import BoardSquare, Movement

T = TIGER_PLAYER
G = GOAT_PLAYER


class TestAllowedTigerMovements(TestCase):
    def test_base_board_movements(self):
        expected = [
            Movement(BoardSquare(0, 0), BoardSquare(0, 1)),
            Movement(BoardSquare(0, 0), BoardSquare(1, 0)),
            Movement(BoardSquare(0, 0), BoardSquare(1, 1)),
            Movement(BoardSquare(0, 4), BoardSquare(0, 3)),
            Movement(BoardSquare(0, 4), BoardSquare(1, 4)),
            Movement(BoardSquare(0, 4), BoardSquare(1, 3)),
            Movement(BoardSquare(4, 0), BoardSquare(3, 0)),
            Movement(BoardSquare(4, 0), BoardSquare(4, 1)),
            Movement(BoardSquare(4, 0), BoardSquare(3, 1)),
            Movement(BoardSquare(4, 4), BoardSquare(4, 3)),
            Movement(BoardSquare(4, 4), BoardSquare(3, 4)),
            Movement(BoardSquare(4, 4), BoardSquare(3, 3)),
        ]

        game = Game()
        game.game_state.player = TIGER_PLAYER

        self.assertCountEqual(game.available_moves(), expected)

    def test_non_empty_board_movements(self):
        expected = [
            # T1
            Movement(BoardSquare(0, 0), BoardSquare(0, 1)),
            Movement(BoardSquare(0, 0), BoardSquare(1, 0)),
            # T2
            Movement(BoardSquare(1, 1), BoardSquare(0, 1)),
            Movement(BoardSquare(1, 1), BoardSquare(0, 2)),
            Movement(BoardSquare(1, 1), BoardSquare(1, 0)),
            Movement(BoardSquare(1, 1), BoardSquare(1, 2)),
            Movement(BoardSquare(1, 1), BoardSquare(2, 0)),
            Movement(BoardSquare(1, 1), BoardSquare(2, 1)),
            Movement(BoardSquare(1, 1), BoardSquare(2, 2)),
            # T3
            Movement(BoardSquare(4, 0), BoardSquare(3, 0)),
            Movement(BoardSquare(4, 0), BoardSquare(3, 1)),
            # T4
            Movement(BoardSquare(4, 1), BoardSquare(3, 1)),
            Movement(BoardSquare(4, 1), BoardSquare(4, 2)),
        ]

        game = Game()
        game.game_state.player = TIGER_PLAYER
        game.board[0, 4] = 0
        game.board[1, 1] = TIGER_PLAYER
        game.board[4, 4] = 0
        game.board[4, 1] = TIGER_PLAYER

        self.assertCountEqual(game.available_moves(), expected)


class TestAllowedGoatMovements(TestCase):
    def test_goat_movements(self):
        goats_positions = [
            BoardSquare(0, 1),
            BoardSquare(0, 2),
            BoardSquare(2, 2),
            BoardSquare(3, 3),
        ]

        game = Game()
        game.game_state.positioned_goats = TOTAL_NUMBER_OF_GOATS

        expected = [
            # G1
            Movement(BoardSquare(0, 1), BoardSquare(1, 1)),
            # G2
            Movement(BoardSquare(0, 2), BoardSquare(0, 3)),
            Movement(BoardSquare(0, 2), BoardSquare(1, 1)),
            Movement(BoardSquare(0, 2), BoardSquare(1, 2)),
            Movement(BoardSquare(0, 2), BoardSquare(1, 3)),
            # G3
            Movement(BoardSquare(2, 2), BoardSquare(1, 1)),
            Movement(BoardSquare(2, 2), BoardSquare(1, 2)),
            Movement(BoardSquare(2, 2), BoardSquare(1, 3)),
            Movement(BoardSquare(2, 2), BoardSquare(2, 1)),
            Movement(BoardSquare(2, 2), BoardSquare(2, 3)),
            Movement(BoardSquare(2, 2), BoardSquare(3, 1)),
            Movement(BoardSquare(2, 2), BoardSquare(3, 2)),
            Movement(BoardSquare(3, 3), BoardSquare(2, 3)),
            # G4
            Movement(BoardSquare(3, 3), BoardSquare(2, 4)),
            Movement(BoardSquare(3, 3), BoardSquare(3, 2)),
            Movement(BoardSquare(3, 3), BoardSquare(3, 4)),
            Movement(BoardSquare(3, 3), BoardSquare(4, 2)),
            Movement(BoardSquare(3, 3), BoardSquare(4, 3)),
        ]
        for goat in goats_positions:
            game.board[goat.lin, goat.col] = GOAT_PLAYER
        self.assertCountEqual(game.available_moves(), expected)

    def test_goat_positioning_movements(self):
        """Must allow only movements of goat positioning"""
        goats_positions = [
            BoardSquare(0, 1),
            BoardSquare(0, 2),
            BoardSquare(2, 2),
            BoardSquare(3, 3),
        ]

        # Must allow all empty positions
        expected = [
            BoardSquare(0, 3),
            BoardSquare(1, 0),
            BoardSquare(1, 1),
            BoardSquare(1, 2),
            BoardSquare(1, 3),
            BoardSquare(1, 4),
            BoardSquare(2, 0),
            BoardSquare(2, 1),
            BoardSquare(2, 3),
            BoardSquare(2, 4),
            BoardSquare(3, 0),
            BoardSquare(3, 1),
            BoardSquare(3, 2),
            BoardSquare(3, 4),
            BoardSquare(4, 1),
            BoardSquare(4, 2),
            BoardSquare(4, 3),
        ]

        game = Game()
        game.game_state.positioned_goats = 0
        for goat in goats_positions:
            game.board[goat.lin, goat.col] = GOAT_PLAYER

        self.assertCountEqual(game.available_moves(), expected)
