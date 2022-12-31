import builtins

import numpy as np

from game_state import VnChessState

# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000


def evaluation(node):
    score = np.sum(node.board)
    return score


class Node(VnChessState):

    def __init__(self, _prev_board, _board, _player_num, _parent=None, _action=None):
        super().__init__(_prev_board, _board, _player_num)
        self.parent = _parent
        self.action = _action
        self.children: list[Node] = []
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

    def move(self, action: tuple[tuple[int], tuple[int]]):
        state = super().move(action)
        return Node(state.prev_board, state.board, state.player_num)


def minimax(node: Node, is_max_player, alpha, beta, depth, max_depth=3, count_node=0):
    if depth == max_depth:
        return node.get_value(), count_node

    best, choose = (MIN, builtins.max) if is_max_player else (MAX, builtins.min)

    list_action = node.get_all_legal_actions()
    np.random.shuffle(list_action)

    for action in list_action:
        child = node.move(action)

        # Count number of explore node
        count_node += 1

        node.append_child(child, action)
        value, count_node = minimax(child, not is_max_player, alpha, beta, depth + 1, max_depth, count_node)
        best = choose(best, value)

        node.set_value(best)

        if is_max_player:
            alpha = choose(best, alpha)
        else:
            beta = choose(best, beta)

        if alpha >= beta:
            break

    node.set_value(best)
    return best, count_node


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=3)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None


def move_depth_3(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=3)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None


def move_depth_4(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=4)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None


def move_depth_5(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=5)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None
