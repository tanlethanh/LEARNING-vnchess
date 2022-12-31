from action import Action
import numpy as np


def print_board(_board):
    for i in range(len(_board)).__reversed__():
        for j in range(len(_board[0])):
            if _board[i][j] == 1:
                print("X", end="\t")
            elif _board[i][j] == -1:
                print("O", end="\t")
            elif _board[i][j] == 0:
                print("_", end="\t")
            else:
                print("^", end="\t")
        print("\n")


def print_action_matrix(_matrix: list[list[list[Action]]]):
    for row in _matrix[:].__reversed__():
        for ele in row:
            action = (' '.join([str(ac) for ac in ele]))
            print(action, end="\t")
        print("\n")


def create_action_matrix():
    action_matrix = [[[]] * 5] * 5
    for i in range(0, 5):
        for j in range(0, 5):
            action_matrix[i][j] = get_avail_actions((i, j))
    return action_matrix


def blind_move(pos: tuple[int, int], action: Action):
    x, y = pos
    move_x, move_y = action.value
    return x + move_x, y + move_y


def get_at(board: list[list[int]], pos: tuple[int, int]):
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


def get_avail_half_actions(position) -> list[Action]:
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


def is_valid_position(pos: tuple[int, int]) -> bool:
    x, y = pos
    return 0 <= x <= 4 and 0 <= y <= 4


def get_player_position(board: list[list[int]], player_num: int) -> list[tuple[int, int]]:
    w, h = len(board), len(board[0])
    res = []
    for i in range(w):
        for j in range(h):
            if board[i][j] == player_num:
                res.append((i, j))
    return res


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
            if _prev_board[i][j] == _player_num and _board[i][j] == 0:
                active_position = i, j

            count_board += _board[i][j]

    if with_count_board:
        return active_position, is_possibility_trap, count_board

    return active_position, is_possibility_trap


def get_traps(board, active_pos, player_num) -> list[tuple[tuple[int, int]]]:
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

    # traps = []
    # for action in get_avail_actions(active_pos):
    #     adjacent_pos = blind_move(active_pos, action)
    #     adjacent_num = get_at(board, adjacent_pos)
    #
    #     if adjacent_num == 0:
    #         starts = []
    #         next_pos = blind_move(adjacent_pos, action)
    #         if (get_at(board, next_pos) == -player_num):
    #
    #             for sub_action in get_avail_actions(adjacent_pos):
    #                 player_pos = blind_move(adjacent_pos, sub_action)
    #                 if (get_at(board, player_pos)) == player_num:
    #                     starts.append(player_pos)
    #
    #         if len(starts) > 0:
    #             traps += [(start, adjacent_pos) for start in starts]

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
    if check_valid:
        i, j = _start
        if _board[i][j] != _player_num:
            print(_board[i][j])
            print(_player_num)
            raise Exception("Start position is not valid")

        active_position, is_possibility_trap = False, False
        if _prev_board is not None:
            active_position, is_possibility_trap = get_active_position(_prev_board, _board, -_player_num)

        # Get all actions of chessman list pair (start, action)
        chessman_actions = []
        if is_possibility_trap and active_position is not None:
            chessman_actions = get_traps(_board, active_position, _player_num)  # [(start, end)]

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
