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
    while int(selected_move) >= len(moves) or int(selected_move) < 0:
        selected_move = input("Choose a move: ")

    return moves[int(selected_move)]


if __name__ == "__main__":
    # play_alg_vs_alg(cutoff_1=5, h_1=heuristic, cutoff_2=5, h_2=heuristic)
    play_human_vs_alg(TIGER_PLAYER, heuristic, 4)
