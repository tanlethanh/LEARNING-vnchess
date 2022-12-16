import sys
import time

import game_manager

if __name__ == "__main__":
    board = game_manager.get_init_board()
    player_num = 1

    prev_board = game_manager.copy_board(board)

    test_mode = "None"

    if len(sys.argv) > 1:
        test_mode = sys.argv[1]

    print(f"Test mode: {test_mode}")
    if test_mode == '2_traps':
        prev_board = [[1, 1, 1, 1, 1],
                      [1, 0, 0, 0, 1],
                      [1, -1, -1, 0, -1],
                      [-1, 0, 0, 0, -1],
                      [-1, 0, 0, -1, -1]]

        board = [[1, 1, 0, 1, 1],
                 [1, 0, 1, 0, 1],
                 [1, -1, -1, 0, -1],
                 [-1, 0, 0, 0, -1],
                 [-1, 0, 0, -1, -1]]
        player_num = -1

    elif test_mode == 'surround_and_kill':
        prev_board = [[1, 1, -1, 1, 1],
                      [1, 0, 0, 0, 1],
                      [1, 0, 1, -1, -1],
                      [0, 0, 0, 0, 0],
                      [-1, -1, -1, -1, -1]]

        board = [[1, 1, -1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [1, 0, 1, -1, -1],
                 [0, 0, 0, 0, 0],
                 [-1, -1, -1, -1, -1]]

        player_num = -1

    game_manager.play_game(prev_board, board, player_num)
