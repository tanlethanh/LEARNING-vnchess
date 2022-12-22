import sys
import time

import game_manager
import minimax

if __name__ == "__main__":
    board = game_manager.get_init_board()
    player_num = 1

    prev_board = game_manager.copy_board(board)

    test_mode = "None"

    if len(sys.argv) > 1:
        test_mode = sys.argv[1]

    print(f"Test mode: {test_mode}")

    game_manager.play_game(prev_board, board, player_num, _move1=minimax.move)
