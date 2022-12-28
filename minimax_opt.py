import builtins
import copy

import numpy as np

from game_manager import get_surrounded_chesses, surround, update_board
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

    def get_value(self, bias=0):
        if self.value is None:
            self.value = evaluation(self) + bias
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

        # This method will change value in _board
        _board = copy.deepcopy(self.board)
        start, end = action
        updated_board = update_board(self.prev_board, copy.deepcopy(_board), start, end, self.player_num,
                                     check_valid=False)

        return Node(_board, updated_board, -self.player_num)


def minimax(node: Node, is_max_player, alpha, beta, depth, max_depth=3, count_node=0, root_player=-2):
    if depth == max_depth:
        return node.get_value(), count_node
        # return node.get_value(depth * node.player_num / max_depth * -1), count_node

    best, choose = (MIN, builtins.max) if is_max_player else (MAX, builtins.min)

    list_action, count_board = node.get_all_legal_actions(with_count=True)

    if depth == 0:
        root_player = node.player_num

    if depth > 0:
        # Near priority just use when exceed 14 (15 - 1) mean that nearing end game
        # Decrease threshold may cut the heuristic
        # if (is_max_player and (count_board * node.player_num >= 16 * node.player_num)) or len(list_action) == 0:
        #     best = count_board + ((max_depth - depth) / (max_depth + 1))
        #     print(f"\t\tNear priority handle at depth: {depth}, best: {best} (Just for X player)")

        if (node.player_num == root_player and count_board * node.player_num >= 16) or len(list_action) == 0:
            best = count_board + ((max_depth - depth) / (max_depth + 1))
            print(f"\t\tNear priority handle at depth: {depth}, best: {best}")

    np.random.shuffle(list_action)

    for action in list_action:
        child = node.move(action)

        # Count number of explore node
        count_node += 1

        node.append_child(child, action)
        value, count_node = minimax(child, not is_max_player, alpha, beta, depth + 1, max_depth, count_node,
                                    root_player)
        best = choose(best, value)

        node.set_value(best)

        if is_max_player:
            alpha = choose(best, alpha)
        else:
            beta = choose(best, beta)

        # Pruning here
        if alpha >= beta:
            break

    node.set_value(best)
    return best, count_node


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=5)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # if np.sum(np.array(_board)) * _player >= 14:
            #     print("DEBUG")
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    print("OPTIMAL MINIMAX")
    print(max_value)
    print([ele.value for ele in cur_node.children])

    return None
