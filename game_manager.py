import sys
import traceback

from utils import print_board, get_active_position, get_traps, copy_board, update_board
from testcase import test_case_steps
import time


def get_start():
    xy = input("\tStart (x,y): ")
    x, y = tuple(xy.split(','))
    x, y = int(x), int(y)

    return x, y


def get_end():
    xy = input("\tEnd (x,y): ")
    x, y = tuple(xy.split(','))
    x, y = int(x), int(y)

    return x, y


def get_init_board():
    return [[1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, -1],
            [-1, 0, 0, 0, -1],
            [-1, -1, -1, -1, -1]]


def check_winner(_board: list[list[int]]):
    total = 0
    for row in _board:
        for ele in row:
            total = total + ele

    if total == 16:
        return 1
    elif total == -16:
        return -1
    else:
        return 0


def input_move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    try:
        start, end = test_case_steps.pop(0)
        return start, end
    except Exception as e:
        print(e)
        print("END Testcase")

    active_position, is_possibility_trap = get_active_position(_prev_board, _board, -_player)

    # Get all actions of chessman list pair (start, action)
    chessman_actions = []
    if is_possibility_trap and active_position is not None:
        chessman_actions = get_traps(_board, active_position, _player)

    if len(chessman_actions) > 0:
        print("\tInput move")
        print(f"\t\t Traps: {chessman_actions}")

    while True:
        try:
            start, end = get_start(), get_end()
            break
        except Exception as e:
            print("\n--------------------------------")
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            print("--------------------------------\n")
            print(f"Play again {_player}\n")

    return start, end


def change_player(_cur_player):
    return -_cur_player


def summary_after_round(board):
    count_x = 0
    count_o = 0
    for row in board:
        for ele in row:
            if ele == 1:
                count_x += 1
            elif ele == -1:
                count_o += 1

    return count_x, count_o


def play_game(prev_board, board, cur_player, _move1=input_move, _move2=input_move, print_out=True):
    duration_1 = 1000000000000.0
    duration_2 = 1000000000000.0
    print("--------------------------- Game start ---------------------------\n")
    print(f"Active position: {get_active_position(prev_board, board, -cur_player)}")

    print("Previous board")
    # print_board(prev_board)

    print("Current board")
    print_board(board)

    # count round
    x_turn = 0
    o_turn = 0
    x_time = 0
    o_time = 0

    while check_winner(board) == 0 and duration_1 > 0 and duration_2 > 0:

        if print_out:
            print(f"Player: {'X' if cur_player == 1 else 'O'}")

        if cur_player == 1:
            x_turn += 1
            start_time = time.time()
            start, end = _move1(copy_board(prev_board), copy_board(board), cur_player,
                                _remain_time_x=duration_1, _remain_time_o=duration_2)
            end_time = time.time()

            exec_time = end_time - start_time
            duration_1 -= exec_time
            x_time += exec_time

            if print_out:
                print("Time taked: {:3f}".format(end_time - start_time))

            if exec_time >= 3:
                print(f"X player exec time exceed 3s | execution time = {exec_time}")

        elif cur_player == -1:
            o_turn += 1
            start_time = time.time()
            start, end = _move2(copy_board(prev_board), copy_board(board), cur_player,
                                _remain_time_x=duration_1, _remain_time_o=duration_2)
            end_time = time.time()
            if print_out:
                print("Time taked: {:3f}".format(end_time - start_time))
            exec_time = (end_time - start_time)

            duration_2 -= exec_time
            o_time += exec_time

            if exec_time >= 3:
                print(f"O player exec time exceed 3s | execution time = {exec_time}")

        else:
            raise Exception(f"\tCurrent player is not valid {cur_player}")
        try:
            cp_board = copy_board(board)
            board = update_board(prev_board, board, start, end, cur_player)
            prev_board = cp_board
        except Exception as e:
            print("\n--------------------------------")
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            print("--------------------------------\n")
            print(f"Play again {cur_player}\n")
            continue

        x_chessman, o_chessman = summary_after_round(board)

        if x_chessman >= 14:
            print_board(board)

        # time.sleep(1)
        # os.system('cls')
        # print_board(board)
        print(f"\tTotal in board: {x_chessman - o_chessman}\t X: {x_chessman}\t O: {o_chessman}")
        cur_player = change_player(cur_player)

    if duration_1 <= 0 or duration_2 <= 0:
        print("Time out, draw")
        exit()
    winner = check_winner(board)
    winner = "X" if winner == 1 else ("O" if winner == -1 else "None")
    print(f"\n\n⭐ ⭐ ⭐ Winner {winner} ⭐ ⭐ ⭐")
    print(f"X turn: {x_turn}")
    print(f"X time: {x_time}")
    print(f"O turn: {o_turn}")
    print(f"O time: {o_time}")
    print("\n--------------------------- Game stop ---------------------------\n\n")

    return winner
