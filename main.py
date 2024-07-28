from constants import TIGER_PLAYER
from game.game import Game


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


if __name__ == "__main__":
    main()
