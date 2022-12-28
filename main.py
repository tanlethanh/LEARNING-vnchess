import copy
import sys
import time

import game_manager
import minimax
import monte
import random_move
import temp
import minimax_agent
import minimax_opt

if __name__ == "__main__":
    board = game_manager.get_init_board()
    player_num = 1

    prev_board = None
    test_mode = "None"

    if len(sys.argv) > 1:
        test_mode = sys.argv[1]

    try:
        num_round = int(sys.argv[2])
    except:
        num_round = 1

    try:
        use_spec_board = bool(sys.argv[3])
    except:
        use_spec_board = False


    x_win = 0
    o_win = 0

    print(f"Test mode: {test_mode}")

    for i in range(num_round):
        prev_board = None

        if use_spec_board:
            board = copy.deepcopy(temp.test_board_3)
        else:
            board = game_manager.get_init_board()

        if test_mode == "minimax_random":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax.move, _move2=random_move.move)
        elif test_mode == "minimax_monte":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax.move, _move2=monte.move)
        elif test_mode == "monte_random":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=monte.move, _move2=random_move.move)
        elif test_mode == "minimax_minimax":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax_opt.move,
                                            _move2=minimax.move_depth_3, print_out=False)

        elif test_mode == "minimax_all":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax_agent.move_all,
                                            _move2=minimax.move_depth_4)
        elif test_mode == "minimax_opt":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax_opt.move,
                                            _move2=minimax.move_depth_5,
                                            print_out=False)

        elif test_mode == "minimax_same":
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax.move_depth_3,
                                            _move2=minimax.move_depth_3,
                                            print_out=False)

        elif test_mode == "spec":
            board = temp.test_board
            prev_board = game_manager.copy_board(temp.test_board)
            winner = game_manager.play_game(prev_board, board, player_num, _move1=minimax.move)

        if winner == "X":
            x_win += 1
        elif winner == "O":
            o_win += 1
        print("\n\n\n---------------- Summary ----------------\n")
        print(f"Number of round: {num_round}")
        print(f"X win: {x_win}")
        print(f"O win: {o_win}")
        print("Version: "
              "Just affect to max step, add padding depth, nearing winner"
              "Affect count >= 14"
              "")
