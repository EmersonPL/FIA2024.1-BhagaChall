import time

from numpy import argmax, argmin

from minimax.heuristics import heuristic
from minimax.minimax import alpha_beta_search
from minimax.search_tree import SearchTree
from src.constants import GOAT_PLAYER, TIGER_PLAYER
from src.game.game import Game


def main():
    game = Game()
    while not game.is_game_over():
        moves = game.available_moves()
        print(f"Allowed moves:")
        for i, move in enumerate(moves):
            print(f"{i}: {move}")

        print()
        selected_move = input("Choose a move: ")
        while int(selected_move) >= len(moves):
            selected_move = input("Choose a move: ")

        move = moves[int(selected_move)]
        game.ply(move)

        game.print_game_info()

    winner = game.get_winner()
    winner = "Tiger" if winner == TIGER_PLAYER else "Goat"
    print(f"Winner: {winner}")


def play_alg_vs_alg(h_1=None, cutoff_1=None, h_2=None, cutoff_2=None):
    game = Game()
    while not game.is_game_over():
        print(
            f"\nPlayer: {'Cabra' if game.game_state.player == GOAT_PLAYER else 'Tigre'}\n"
        )
        start = time.time()
        if game.game_state.player == GOAT_PLAYER:
            node: SearchTree = alpha_beta_search(
                game=game,
                cutoff=cutoff_1,
                heuristic=h_1,
            )
            best_move = argmax([children.value for children in node.children])
        else:
            node: SearchTree = alpha_beta_search(
                game=game,
                cutoff=cutoff_2,
                heuristic=h_2,
            )
            best_move = argmin([children.value for children in node.children])
        move = node.children[best_move].move

        game.ply(move)
        end = time.time()
        print(f"Time: {end - start:.5f}")
        print(f"Selected move: {move}")
        print("-" * 80)

    print("*" * 80)
    print(game.print_game_info())
    result = game.get_winner()
    if result == GOAT_PLAYER:
        print("Cabra venceu")
    else:
        print("Tigre venceu")


def play_human_vs_alg(
    human_player: int = GOAT_PLAYER, heuristic=None, cutoff=None
):
    game = Game()
    while not game.is_game_over():
        print(
            f"\nPlayer: {'Cabra' if game.game_state.player == GOAT_PLAYER else 'Tigre'}\n"
        )
        if human_player == game.game_state.player:
            selected_move = _select_move(game)
            game.ply(selected_move)
        else:
            start = time.time()
            node: SearchTree = alpha_beta_search(
                game=game,
                cutoff=cutoff,
                heuristic=heuristic,
            )
            best_move = argmax([children.value for children in node.children])

            move = node.children[best_move].move

            game.ply(move)
            end = time.time()
            print(f"Time: {end - start:.5f}")

            print(f"Selected move: {move}")
            print("-" * 80)

    print("*" * 80)
    print(game.print_game_info())
    result = game.get_winner()
    if result == GOAT_PLAYER:
        print("Cabra venceu")
    else:
        print("Tigre venceu")


def _select_move(game):
    moves = game.available_moves()
    print(game.print_game_info())
    print(f"Allowed moves:")
    for i, move in enumerate(moves):
        print(f"{i}: {move}")

    print()
    selected_move = input("Choose a move: ")
    while (
        not selected_move.isdigit()
        or int(selected_move) >= len(moves)
        or int(selected_move) < 0
    ):
        selected_move = input("Choose a move: ")

    return moves[int(selected_move)]


def _select_cutoff():
    selected_depth = input("The depth must be a positive integer: ")
    while not selected_depth.isdigit() or int(selected_depth) < 1:
        selected_depth = input("The depth must be a positive integer: ")

    return int(selected_depth)


if __name__ == "__main__":
    print("1: Computer x Computer\n" "2: Player x Computer\n")
    selected_mode = input("Choose a mode: ")
    while (
        not selected_mode.isdigit()
        or int(selected_mode) > 2
        or int(selected_mode) < 0
    ):
        selected_mode = input("Choose a mode: ")

    if int(selected_mode) == 1:
        print("Select search depth for the first player")
        cutoff_1 = _select_cutoff()
        print("Select search depth for the second player")
        cutoff_2 = _select_cutoff()
        play_alg_vs_alg(
            cutoff_1=cutoff_1, h_1=heuristic, cutoff_2=cutoff_2, h_2=heuristic
        )
    else:
        print("Select search depth for the computer player")
        cutoff = _select_cutoff()

        print("1: Play as GOAT\n" "2: Play as TIGER\n")
        selected_mode = input("Choose your pieces: ")
        while (
            not selected_mode.isdigit()
            or int(selected_mode) > 2
            or int(selected_mode) < 0
        ):
            selected_mode = input("Choose your pieces: ")

        if int(selected_mode) == 1:
            play_human_vs_alg(GOAT_PLAYER, heuristic, cutoff)
        else:
            play_human_vs_alg(TIGER_PLAYER, heuristic, cutoff)
