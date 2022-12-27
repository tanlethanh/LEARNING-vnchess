# Python3 program to demonstrate
# working of Alpha-Beta Pruning
import builtins
import sys

import numpy as np

from action import Action
from game_manager import get_active_position, get_traps, get_actions_of_chessman, copy_board, update_board
from utils import blind_move

# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000


def evaluation(node):
    score = np.sum(node.board)
    # if score == 16:
    #     print("-------------------------------------- WIN --------------------------------------")
    #     sys.exit()
    return score


class Node:

    def __init__(self, _prev_board, _board, _player_num, _parent=None, _action=None):
        self.parent = _parent
        self.action = _action
        self.children: list[Node] = []
        self.prev_board: list[list] = _prev_board
        self.board: list[list] = _board
        self.player_num = _player_num
        self.value = None

    def get_value(self):
        if self.value is None:
            self.value = evaluation(self)
        return self.value

    def set_value(self, value):
        self.value = value

    def append_child(self, child, action):
        if not isinstance(child, Node):
            raise Exception("Type must be Node")

        child.parent = self
        child.action = action
        self.children.append(child)


def get_all_actions(_prev_board, _board, _player_num):
    """
    Action result is tuple(start, end)

    :param _prev_board:
    :param _board:
    :param _player_num:
    :return:
    """

    all_actions: list[tuple[tuple[int, int]]] = []
    active_position, is_possibility_trap, prev_position = get_active_position(_prev_board, _board, -_player_num)

    # Get all actions of chessman list pair (start, action)
    if is_possibility_trap and active_position is not None and prev_position:
        all_actions = get_traps(_board, active_position, _player_num, prev_position)

    if not is_possibility_trap or len(all_actions) == 0:
        for i in range(len(_board)):
            for j in range(len(_board[0])):
                if _board[i][j] == _player_num:
                    actions = get_actions_of_chessman(_board, (i, j))
                    all_actions += [((i, j), blind_move((i, j), action)) for action in actions]

    np.random.shuffle(all_actions)
    return all_actions


def take_action(_prev_board, _board, _player_num, _action):
    # This method will change value in _board
    _board = copy_board(_board)

    start, end = _action
    updated_board = update_board(_prev_board, copy_board(_board), start, end, _player_num)

    # print(f"In MINIMAX: _player_num: {_player_num}")
    return Node(_board, updated_board, -_player_num)


def minimax(node: Node, is_max_player, alpha, beta, depth, max_depth=5):
    if depth == max_depth:
        return node.get_value()

    # if is_max_player:
    #     print("MAX phase")
    # else:
    #     print("MIN phase")

    best, choose = (MIN, builtins.max) if is_max_player else (MAX, builtins.min)

    list_action = get_all_actions(node.prev_board, node.board, node.player_num)

    if len(list_action) == 0:
        print("End game here")

    for action in list_action:
        child = take_action(node.prev_board, node.board, node.player_num, action)
        node.append_child(child, action)
        value = minimax(child, not is_max_player, alpha, beta, depth + 1, max_depth)
        best = choose(best, value)

        node.set_value(best)

        if is_max_player:
            alpha = choose(best, alpha)
        else:
            beta = choose(best, beta)

        if alpha >= beta:
            # print(f"Pruning: alpha = {alpha}, beta: {beta}")
            break

    node.set_value(best)
    return best


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=5)

    # print(max_value)
    # print([child.get_value() for child in cur_node.children])
    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            print(f"\t MINIMAX move: {start} -> {end}")
            print((start, end))
            return child.action

    return None


def move_depth_3(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=3)

    # print(max_value)
    # print([child.get_value() for child in cur_node.children])
    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None


def move_depth_4(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=4)

    # print(max_value)
    # print([child.get_value() for child in cur_node.children])
    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None
