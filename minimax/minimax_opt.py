import builtins
import copy
import numpy as np

from utils import blind_move, get_actions_of_chessman, update_board, get_active_position, get_traps

BOARD_SIZE = 5
# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000


# Utils


# Game state
class VnChessState:

    def __init__(self, prev_board=None, board=None, player_num=1):
        '''
        state: chess board
        '''
        self.prev_board = prev_board
        self.board = board
        self.player_num = player_num

    @property
    def game_result(self) -> int:
        value = (np.sum(np.array(self.board)))
        if value > 0:
            return 2
        elif value == 0:
            return 1
        else:
            return 0

    def is_game_over(self) -> bool:
        x = np.sum(np.array(self.board))
        return x == 16 or x == -16

    def get_all_legal_actions(self, with_count=False):
        """
        Action result is tuple(start, end)

        """

        all_actions: list[tuple[tuple[int, int]]] = []

        if with_count:
            active_position, is_possibility_trap, count_board = get_active_position(self.prev_board, self.board,
                                                                                    -self.player_num, with_count)
        else:
            active_position, is_possibility_trap = get_active_position(self.prev_board, self.board, -self.player_num)

        # Get all actions of chessman list pair (start, action)
        if is_possibility_trap and active_position is not None:
            all_actions = get_traps(self.board, active_position, self.player_num)

        if not is_possibility_trap or len(all_actions) == 0:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == self.player_num:
                        actions = get_actions_of_chessman(self.board, (i, j))
                        all_actions += [((i, j), blind_move((i, j), action)) for action in actions]

        if with_count:
            return all_actions, count_board
        return all_actions

    def move(self, action: tuple[tuple[int], tuple[int]]):
        # This method will change value in _board
        _board = copy.deepcopy(self.board)
        start, end = action
        updated_board = update_board(self.prev_board, copy.deepcopy(_board), start, end, self.player_num,
                                     check_valid=False)
        return VnChessState(_board, updated_board, -self.player_num)


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
            best = count_board + ((max_depth - depth) / (max_depth + 1)) * root_player
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
