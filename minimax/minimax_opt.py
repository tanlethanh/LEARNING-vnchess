import builtins
import copy
import time
from enum import Enum
import numpy as np

BOARD_SIZE = 5
# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000


class Action(Enum):
    MOVE_UP = (1, 0)
    MOVE_DOWN = (-1, 0)
    MOVE_LEFT = (0, -1)
    MOVE_RIGHT = (0, 1)
    MOVE_UP_LEFT = (1, -1)
    MOVE_DOWN_RIGHT = (-1, 1)
    MOVE_UP_RIGHT = (1, 1)
    MOVE_DOWN_LEFT = (-1, -1)

    def __str__(self) -> str:
        if self == Action.MOVE_UP:
            return "↑"
        elif self == Action.MOVE_DOWN:
            return "↓"
        elif self == Action.MOVE_LEFT:
            return "←"
        elif self == Action.MOVE_RIGHT:
            return "→"
        elif self == Action.MOVE_UP_LEFT:
            return "↖"
        elif self == Action.MOVE_DOWN_RIGHT:
            return "↘"
        elif self == Action.MOVE_UP_RIGHT:
            return "↗"
        elif self == Action.MOVE_DOWN_LEFT:
            return "↙"

    def get_opposite(self):
        x, y = self.value
        return Action((-x, -y))

    @staticmethod
    def get_half_actions():
        return [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_UP_RIGHT, Action.MOVE_UP_LEFT]

    def __eq__(self, __o: object) -> bool:
        return self.value == __o.value


def sum_board(_board):
    sum_board = 0
    for row in _board:
        for ele in row:
            sum_board += ele

    return sum_board


def is_valid_position(pos) -> bool:
    """
    Check position is in board or not
    :param pos:
    :return:
    """
    x, y = pos
    return 0 <= x <= 4 and 0 <= y <= 4


def get_at(board, pos):
    """
    This method get value in chess board at x, y position.

    :return: board[x][y] or None if position is invalid
    """
    x, y = pos
    if not ((0 <= x < 5) and (0 <= y < 5)):
        return None
    return board[x][y]


def get_avail_actions(position):
    x, y = position
    index_sum = x + y
    if index_sum % 2 == 0:
        valid_actions = list(Action)
    else:
        valid_actions = [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]
    result = []
    for action in valid_actions:
        end = blind_move(position, action)
        if is_valid_position(end):
            result.append(action)
    return result


def get_avail_half_actions(position):
    x, y = position
    index_sum = x + y
    if index_sum % 2 == 0:
        valid_actions = Action.get_half_actions()
    else:
        valid_actions = [Action.MOVE_UP, Action.MOVE_RIGHT]
    result = []
    for action in valid_actions:
        end = blind_move(position, action)
        if is_valid_position(end):
            result += [action]
    return result


def get_traps(board, active_pos, player_num):
    # TODO: Exact trap from last move of opponent
    # Result shape [(start_pos, action)]

    traps = []
    for action in get_avail_half_actions(active_pos):
        assert (isinstance(action, Action))
        pos_1, pos_2 = blind_move(active_pos, action), blind_move(active_pos, action.get_opposite())
        num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)
        if num_1 == num_2 == -player_num:
            for sub_action in get_avail_actions(active_pos):
                adjacent_pos = blind_move(active_pos, sub_action)
                adjacent_num = get_at(board, adjacent_pos)
                if adjacent_num == player_num:
                    traps += [(adjacent_pos, active_pos)]

    return traps


def get_active_position(_prev_board, _board, _player_num: int,
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
            return None, False, sum_board(_board)
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
            if _prev_board[i][j] == _player_num and _board[i][j] == 0:
                active_position = i, j

            count_board += _board[i][j]

    if with_count_board:
        return active_position, is_possibility_trap, count_board

    return active_position, is_possibility_trap


# Utils
def blind_move(pos, action: Action):
    x, y = pos
    move_x, move_y = action.value
    return x + move_x, y + move_y


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
    current_board = copy.deepcopy(board)
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
    This method update board by moving from start to end location. Not check

    Value in _board matrix will be changed,
    make sure the passing _board is a copied board if you don't want to change _board.
    """
    # Update board
    i, j = _end
    _board[i][j] = _player_num

    i, j = _start
    _board[i][j] = 0

    # Ganh truoc, vay sau <- vi co truong hop co ca ganh va vay
    # cap nhat neu co ganh
    for action in Action.get_half_actions():
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


# Game state
def evaluation(node):
    score = sum_board(node.board)
    return score


class VnChessState:

    def __init__(self, prev_board=None, board=None, player_num=1):
        '''
        state: chess board
        '''
        self.prev_board = prev_board
        self.board = board
        self.player_num = player_num

    def get_all_legal_actions(self, with_count=False):
        """
        Action result is tuple(start, end)

        """

        all_actions = []

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

    def move(self, action):
        # This method will change value in _board
        _board = copy.deepcopy(self.board)
        start, end = action
        updated_board = update_board(self.prev_board, copy.deepcopy(_board), start, end, self.player_num,
                                     check_valid=False)
        return VnChessState(_board, updated_board, -self.player_num)


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

    def move(self, action):

        # This method will change value in _board
        _board = copy.deepcopy(self.board)
        start, end = action
        updated_board = update_board(self.prev_board, copy.deepcopy(_board), start, end, self.player_num,
                                     check_valid=False)

        return Node(_board, updated_board, -self.player_num)


def minimax(node: Node, is_max_player, alpha, beta, depth, max_depth=3, count_node=0, root_player=-2, total_duration=0,
            timeout=3):
    start = time.time()

    if depth == max_depth or (timeout - total_duration < 0.1):
        # if timeout - total_duration < 0.1:
        #     print("\t\t\t TIMEOUT")
        end = time.time()
        return node.get_value(), count_node, (end - start)

    best, choose = (MIN, builtins.max) if is_max_player else (MAX, builtins.min)

    list_action, count_board = node.get_all_legal_actions(with_count=True)

    if depth == 0:
        root_player = node.player_num

    if depth > 0:
        # Near priority just use when exceed 16 mean that nearing end game
        # Decrease threshold may cut the heuristic

        if (node.player_num == root_player and count_board * node.player_num >= 16) or len(list_action) == 0:
            best = count_board + ((max_depth - depth) / (max_depth + 1)) * root_player
            # print(f"\t\tNear priority handle at depth: {depth}, best: {best}")

    np.random.shuffle(list_action)

    for action in list_action:
        child = node.move(action)

        # Count number of explore node
        count_node += 1

        node.append_child(child, action)
        value, count_node, duration = minimax(child, not is_max_player, alpha, beta, depth + 1, max_depth,
                                              count_node,
                                              root_player, total_duration)
        total_duration += duration

        # Update for pruning
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
    end = time.time()
    return best, count_node, end - start


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o, max_depth=5):
    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, _, _ = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0, max_depth=max_depth)

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            print(f"\t\t{'X' if _player == 1 else 'O'} choose: {max_value}")
            return child.action

    return None


def move_5(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    return move(_prev_board, _board, _player, _remain_time_x, _remain_time_o, max_depth=5)


def move_6(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    return move(_prev_board, _board, _player, _remain_time_x, _remain_time_o, max_depth=6)


def move_7(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    return move(_prev_board, _board, _player, _remain_time_x, _remain_time_o, max_depth=7)
