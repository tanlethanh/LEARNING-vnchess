from action import Action
from utils import get_at, get_valid_actions, blind_move, get_active_position


class Chess:

    def __init__(self, board):
        pass

    def move_chess_man(self, start: tuple[int, int], action: Action) -> tuple[int, int]:
        """
        This method take a valid action for chess man, action must be checked.

        :param start: position of chosen chess man
        :param action: a
        :return: end position
        """
        # TODO:
        pass

    def get_valid_actions(self, position: tuple[int, int]) -> list[Action]:
        """
        This method return list of all valid actions from a position in the game board
        (don't care about chess man, just position).

        :param position: a position, tuple (x, y)
        :return: list of all valid actions
        """
        pass

    def update_board(self, board: list[list[int]], start: tuple[int, int], action: Action) -> list[list[int]]:
        # TODO
        pass


def move_in_board(board: list[list[int]], index: tuple[int, int], action: Action) \
        -> tuple[tuple[int, int], tuple[int, int]]:
    # TODO
    pass


def get_traps(board, active_pos, player_num) -> list[tuple[tuple[int, int], Action]]:
    # TODO: Exact trap from last move of opponent
    traps = []
    for action in list(Action):
        adjacent_pos = blind_move(active_pos, action)
        adjacent_num = get_at(board, adjacent_pos)

        if adjacent_num == 0:
            starts = []
            is_trap = False

            for sub_action in Action.get_positive_action():
                pos_1, pos_2 = blind_move(adjacent_pos, sub_action), \
                               blind_move(adjacent_pos, sub_action.get_opposite())
                num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)

                if num_1 == -player_num and num_2 == -player_num:
                    is_trap = True

                if num_1 == player_num:
                    starts.append(pos_1)
                if num_2 == player_num:
                    starts.append(pos_2)

            if is_trap and len(starts) > 0:
                traps += [(start, adjacent_pos) for start in starts]

    return traps


def get_all_valid_actions(board, player):
    pass


def choose_action(prev_board, board, player, all_actions):
    pass


def move(prev_board, board, player, remain_time_x, remain_time_o):
    player_num = 1 if player == "X" else -1
    active_position, is_possibility_trap = get_active_position(prev_board, board, player_num)
    all_actions = get_traps(board, active_position, player_num) \
        if is_possibility_trap else get_all_valid_actions(board, player)
    return choose_action(prev_board, board, player, all_actions)
