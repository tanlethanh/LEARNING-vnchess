from action import Action


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
            action_matrix[i][j] = get_valid_actions((i, j))
    return action_matrix


def blind_move(pos: tuple[int, int], action: Action):
    x, y = pos
    if action == Action.MOVE_UP:
        x += 1
    elif action == Action.MOVE_DOWN:
        x -= 1
    elif action == Action.MOVE_LEFT:
        y -= 1
    elif action == Action.MOVE_RIGHT:
        y += 1
    elif action == Action.MOVE_UP_LEFT:
        x += 1
        y -= 1
    elif action == Action.MOVE_DOWN_RIGHT:
        x -= 1
        y += 1
    elif action == Action.MOVE_UP_RIGHT:
        x += 1
        y += 1
    elif action == Action.MOVE_DOWN_LEFT:
        x -= 1
        y -= 1
    return x, y


def get_at(board: list[list[int]], pos: tuple[int, int]):
    """
    This method get value in chess board at x, y position.

    :return: board[x][y] or None if position is invalid
    """
    x, y = pos
    if not ((0 <= x < 5) and (0 <= y < 5)):
        return None
    return board[x][y]


def get_active_position(prev_board: list[list[int]], board: list[list[int]], player_num: int):
    active_position = None
    is_possibility_trap = True
    for i in range(5):
        for j in range(5):
            if prev_board[i][j] == -board[i][j]:
                return None, False
            if prev_board[i][j] == 0 and board[i][j] == player_num:
                active_position = i, j

    return active_position, is_possibility_trap


def get_valid_actions(position):
    x, y = position
    index_sum = x + y
    if index_sum % 2 == 0:
        valid_actions = list(Action)
    else:
        valid_actions = [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]

    if x == 0:
        valid_actions = [action for action in valid_actions if (
                action != Action.MOVE_DOWN and action != Action.MOVE_DOWN_LEFT and action != Action.MOVE_DOWN_RIGHT
        )]
    elif x == 4:
        valid_actions = [action for action in valid_actions if (
                action != Action.MOVE_UP and action != Action.MOVE_UP_LEFT and action != Action.MOVE_UP_RIGHT
        )]

    if y == 0:
        valid_actions = [action for action in valid_actions if (
                action != Action.MOVE_LEFT and action != Action.MOVE_DOWN_LEFT and action != Action.MOVE_UP_LEFT
        )]
    elif y == 4:
        valid_actions = [action for action in valid_actions if (
                action != Action.MOVE_RIGHT and action != Action.MOVE_UP_RIGHT and action != Action.MOVE_DOWN_RIGHT
        )]
    return valid_actions