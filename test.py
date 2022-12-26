import sys
import time
# from game_manager import *
import game_manager
from monte_agent import *

if __name__ == "__main__":
    prev_board = None
    board = game_manager.get_init_board()
    prev_board = None
    human = 1
    bot = -1
    turn = human
    duration_1 = 100.
    duration_2 = 100.
    move = 50
    while True:
        
        print_board(board)
        print("{} turn".format('x' if turn == 1 else 'o'))
        time.sleep(0.5)
        if turn == human:
            time_start = time.time()
            monte = MonteAgent(prev_board, board,human,remain_duration=duration_1, level='easy')
            best_child = monte.move()
            best_move = best_child.parent_action
            start = best_move['pos']
            end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
            time_end = time.time()
            print((best_child.q / best_child.n))
            print(np.sqrt((2 * np.log(best_child.parent.n) / best_child.n)))
            print(best_move)
            print("X start:", start)
            print("X end:", end)
            duration_1 -= (time_end - time_start)
        else:
            time_start = time.time()
            monte = MonteAgent(prev_board, board,bot, remain_duration=duration_2,level='expert')
            best_child = monte.move()
            best_move = best_child.parent_action
            start = best_move['pos']
            end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
            time_end = time.time()
            print((best_child.q / best_child.n))
            print(np.sqrt((2 * np.log(best_child.parent.n) / best_child.n)))
            print(best_move)
            print("O start:", start)
            print("O end:", end)
            duration_2 -= (time_end - time_start)
        prev_board = game_manager.copy_board(board)
        board = game_manager.update_board(prev_board, board, start, end, turn)
        if duration_1 < 0:
            print('player 1 lose, timeout')
            print('player 1 remain duration', duration_1)
            print('player 2 remain duration', duration_2)

            break
        if duration_2 < 0:
            print('player 2 lose, timeout')
            print('player 1 remain duration', duration_1)
            print('player 2 remain duration', duration_2)

            break
        if (check_winner(board) != 0):
            print("{} win".format('x' if turn == 1 else 'o'))
            print('player 1 remain duration', duration_1)
            print('player 2 remain duration', duration_2)

            break
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
