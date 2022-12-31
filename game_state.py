import copy

import numpy as np

from utils import get_traps, get_actions_of_chessman, get_active_position, update_board, blind_move

BOARD_SIZE = 5


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
