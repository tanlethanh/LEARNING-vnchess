import os
import sys
import traceback

import numpy as np

from action import Action
from utils import blind_move, get_at, get_avail_actions, is_valid_position, print_board, get_avail_half_actions
from temp import test_case_steps
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


def copy_board(_board: list[list[int]]):
    if _board is None:
        return None

    copied_board = []
    for row in _board:
        copied_board.append(row[:])

    return copied_board


def get_active_position(_prev_board: list[list[int]], _board: list[list[int]], _player_num: int,
                        with_count_board=False):
    """

    :param _prev_board:
    :param _board:
    :param _player_num: of the player take last move
    :param with_count_board:
    :return:
    """

    if _prev_board == None:
        if with_count_board:
            return None, False, np.sum(np.array(_board))
        else:
            return None, False

    active_position = None
    is_possibility_trap = True

    count_board = 0

    for i in range(5):
        for j in range(5):
            # Nuoc di an quan khong phai la mo
            if _prev_board[i][j] == -_player_num and _board[i][j] == _player_num:
                is_possibility_trap = False
            if _prev_board[i][j] == 0 and _board[i][j] == _player_num:
                active_position = i, j
            if _prev_board[i][j] == _player_num and _board[i][j]==0:
                prev_position = i, j
            count_board += _board[i][j]

    if with_count_board:
        return active_position, is_possibility_trap, count_board

    return active_position, is_possibility_trap


def get_traps(board, active_pos, player_num, prev_position) -> list[tuple[tuple[int, int]]]:
    # TODO: Exact trap from last move of opponent
    # Result shape [(start_pos, action)]
    traps = []
    for action in get_avail_half_actions(prev_position):
        assert(isinstance(action, Action))
        pos_1, pos_2 = blind_move(prev_position, action), blind_move(prev_position, action.get_opposite())
        num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)
        if num_1 == num_2 == -player_num:
            for sub_action in get_avail_actions(prev_position):
                adjacent_pos = blind_move(prev_position, sub_action)
                adjacent_num = get_at(board, adjacent_pos)
                if adjacent_num == player_num:
                    traps += [(adjacent_pos, prev_position)]
        # if adjacent_num == 0:
        #     starts = []
        #     next_pos = blind_move(adjacent_pos, action)
        #     if (get_at(board, next_pos) == -player_num):

        #         for sub_action in get_avail_actions(adjacent_pos):
        #             player_pos = blind_move(adjacent_pos, sub_action)
        #             if (get_at(board, player_pos)) == player_num:
        #                 starts.append(player_pos)

        #     if len(starts) > 0:
        #         traps += [(start, adjacent_pos) for start in starts]

    return traps


def get_actions_of_chessman(_board, _pos):
    """

    :param _board:
    :param _pos:
    :return: list actions move to (0)
    """
    actions = get_avail_actions(_pos)
    actions_of_chessman = []
    for action in actions:
        new_pos = blind_move(_pos, action)
        if int(get_at(_board, pos=new_pos)) == 0:
            actions_of_chessman.append(action)
    return actions_of_chessman


def get_surrounded_chesses(board, player_num):
    # print("Getting surround team")
    current_board = copy_board(board)
    # print(current_board)
    w, h = len(current_board), len(current_board[0])
    teams = []
    for i in range(w):
        for j in range(h):
            if int(current_board[i][j]) == 2:
                continue
            if int(current_board[i][j]) == -player_num:
                # print("current", i, j, current_board[i][j])
                team = []
                explore = []
                explore.append((i, j))
                is_surrounded = True
                while len(explore) != 0:
                    curr_x, curr_y = explore.pop()
                    moves = get_avail_actions((curr_x, curr_y))
                    for move in moves:
                        next_x, next_y = blind_move((curr_x, curr_y), move)
                        if is_valid_position((next_x, next_y)) and int(current_board[next_x][next_y]) != 2 and int(
                                current_board[next_x][next_y]) != player_num:
                            if int(current_board[next_x][next_y]) == 0:
                                is_surrounded = False
                            elif int(current_board[next_x][next_y]) == -player_num:
                                explore.append((next_x, next_y))
                    if is_surrounded:
                        team.append((curr_x, curr_y))
                    current_board[curr_x][curr_y] = 2

                if is_surrounded:
                    teams += team
    # print(f"-------- Surround: {teams}")
    return list(set(teams))


def surround(board, surrounded_teams, new_value):
    for chess_index in surrounded_teams:
        x, y = chess_index
        if board[x][y] != new_value:
            board[x][y] = new_value
    return board


def update_board(_prev_board, _board, _start, _end, _player_num, check_valid=True):
    """
    This method update board by moving from start to end location.
    Raise error if moving is not valid.

    Value in _board matrix will be changed,
    make sure the passing _board is a copied board if you don't want to change _board.

    :param _prev_board:
    :param _board:
    :param _start:
    :param _end:
    :param _player_num:
    :param check_valid:
    :return:
    """
    i, j = _start
    if _board[i][j] != _player_num:
        print(_board[i][j])
        print(_player_num)
        raise Exception("Start position is not valid")

    active_position, is_possibility_trap = False, False
    if _prev_board is not None:
        active_position, is_possibility_trap, prev_position = get_active_position(_prev_board, _board, -_player_num)

    # Get all actions of chessman list pair (start, action)
    chessman_actions = []
    if is_possibility_trap and active_position is not None:
        chessman_actions = get_traps(_board, active_position, _player_num, prev_position) #[(start, end)]

    if not is_possibility_trap or len(chessman_actions) == 0:
        # print("hh")
        actions = get_actions_of_chessman(_board, _start)
        chessman_actions = [(_start, blind_move(_start, action)) for action in actions]

    # Check the _end point is from valid action
    is_valid = False
    for s, e in chessman_actions:
        if _start == s and _end == e:
            is_valid = True
            break
    if not is_valid:
        print(chessman_actions)
        if is_possibility_trap:
            print("trap")
        else:
            print("not trap")
        raise Exception(f"Action is not valid: {_start} -> {_end}")

    i, j = _end
    _board[i][j] = _player_num

    i, j = _start
    _board[i][j] = 0

    # Ganh truoc, vay sau <- vi co truong hop co ca ganh va vay
    # cap nhat neu co ganh
    for action in get_avail_half_actions(_end):
        i1, j1 = blind_move(_end, action)
        i2, j2 = blind_move(_end, action.get_opposite())

        if (is_valid_position((i1, j1)) and is_valid_position((i2, j2))):
            if _board[i1][j1] == _board[i2][j2] == -_player_num:
                # print(f"\tUpdate board: kill at {i1, j1} and {i2, j2}")
                _board[i1][j1] = _player_num
                _board[i2][j2] = _player_num
        # This blind move can go out of board

    # cap nhat neu co vay
    surround_teams = get_surrounded_chesses(_board, _player_num)
    _board = surround(_board, surround_teams, _player_num)

    return _board


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
