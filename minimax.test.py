import sys
import time

import game_manager
import minimax
import random_move
import temp

if __name__ == "__main__":
    board = game_manager.get_init_board()
    player_num = 1

    prev_board = game_manager.copy_board(board)

    test_mode = "None"

    if len(sys.argv) > 1:
        test_mode = sys.argv[1]

    print(f"Test mode: {test_mode}")
    if test_mode == "random":
        game_manager.play_game(prev_board, board, player_num, _move1=minimax.move, _move2=random_move.move)
    elif test_mode == "spec":
        board = temp.test_board
        prev_board = game_manager.copy_board(temp.test_board)
        game_manager.play_game(prev_board, board, player_num, _move1=minimax.move, _move2=random_move.move)
    else:
        game_manager.play_game(prev_board, board, player_num, _move1=minimax.move)
