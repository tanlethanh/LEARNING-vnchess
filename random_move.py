import random
from typing import List, Tuple

import numpy as np

from game_manager import get_active_position, get_traps, get_actions_of_chessman
from utils import blind_move


def get_all_actions(_prev_board, _board, _player_num) -> list[tuple[tuple[int, int]]]:
    """
    Action result is tuple(start, end)

    :param _prev_board:
    :param _board:
    :param _player_num:
    :return:
    """

    all_actions: list[tuple[tuple[int, int]]] = []
    active_position, is_possibility_trap = get_active_position(_prev_board, _board, -_player_num)

    # Get all actions of chessman list pair (start, action)
    if is_possibility_trap and active_position is not None:
        all_actions = get_traps(_board, active_position, _player_num)

    if not is_possibility_trap or len(all_actions) == 0:
        for i in range(len(_board)):
            for j in range(len(_board[0])):
                if _board[i][j] == _player_num:
                    actions = get_actions_of_chessman(_board, (i, j))
                    all_actions += [((i, j), blind_move((i, j), action)) for action in actions]

    np.random.shuffle(all_actions)
    return all_actions


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    actions = get_all_actions(_prev_board, _board, _player)
    start, end = actions[0]

    print(f"\t RANDOM move: {start} -> {end}")
    return start, end
