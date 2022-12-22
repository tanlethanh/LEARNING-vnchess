import sys
import time
# from game_manager import *
import game_manager
from monte_agent import *

if __name__ == "__main__":
    board = game_manager.get_init_board()
    prev_board = None
    human = 1
    bot = -1
    turn = human
    while not game_manager.check_winner(board):
        
        print_board(board)
        time.sleep(1)
        print("{} turn".format('x' if turn == 1 else 'o'))
        if turn == human:
            monte = MonteAgent(board,human,1000)
            best_move = monte.move().parent_action
            start = best_move['pos']
            end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
            print(best_move)
            print("X start:", start)
            print("X end:", end)
        else:
            monte = MonteAgent(board,bot,1000)
            best_move = monte.move().parent_action
            start = best_move['pos']
            end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
            print(best_move)
            print("O start:", start)
            print("O end:", end)
        cp_board = game_manager.copy_board(board)
        board = game_manager.update_board(prev_board, board, start, end, turn)
        prev_board = cp_board
        turn *= -1
        
    # player_num = 1

    # prev_board = game_manager.copy_board(board)

    # test_mode = "None"

    # if len(sys.argv) > 1:
    #     test_mode = sys.argv[1]

    # print(f"Test mode: {test_mode}")
    # if test_mode == '2_traps':
    #     prev_board = [[1, 1, 1, 1, 1],
    #                   [1, 0, 0, 0, 1],
    #                   [1, -1, -1, 0, -1],
    #                   [-1, 0, 0, 0, -1],
    #                   [-1, 0, 0, -1, -1]]

    #     board = [[1, 1, 0, 1, 1],
    #              [1, 0, 1, 0, 1],
    #              [1, -1, -1, 0, -1],
    #              [-1, 0, 0, 0, -1],
    #              [-1, 0, 0, -1, -1]]
    #     player_num = -1

    # elif test_mode == 'surround_and_kill':
    #     prev_board = [[1, 1, -1, 1, 1],
    #                   [1, 0, 0, 0, 1],
    #                   [1, 0, 1, -1, -1],
    #                   [0, 0, 0, 0, 0],
    #                   [-1, -1, -1, -1, -1]]

    #     board = [[1, 1, -1, 1, 1],
    #              [1, 0, 0, 0, 1],
    #              [1, 0, 1, -1, -1],
    #              [0, 0, 0, 0, 0],
    #              [-1, -1, -1, -1, -1]]

    #     player_num = -1
    
    # game_manager.play_game(prev_board, board, player_num)
