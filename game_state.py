import copy

import numpy as np

from game_manager import get_traps, get_actions_of_chessman, get_active_position, update_board
from utils import blind_move

BOARD_SIZE = 4


class VnChessState:

    def __init__(self, parent_state=None, state=None, player_num=1):
        '''
        state: chess board
        '''
        self.prev_board = parent_state
        self.board = state
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

    def get_all_legal_actions(self):
        """
        Action result is tuple(start, end)

        :param _prev_board:
        :param _board:
        :param _player_num:
        :return:
        """

        all_actions: list[tuple[tuple[int, int]]] = []
        active_position, is_possibility_trap = get_active_position(self.prev_board, self.board, -self.player_num)

        # Get all actions of chessman list pair (start, action)
        if is_possibility_trap and active_position is not None:
            all_actions = get_traps(self.board, active_position, self.player_num)

        if not is_possibility_trap or len(all_actions) == 0:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == self.prev_board:
                        actions = get_actions_of_chessman(self.board, (i, j))
                        all_actions += [((i, j), blind_move((i, j), action)) for action in actions]

        return all_actions

    def take_action(_prev_board, _board, _player_num, _action):
        # This method will change value in _board
        _board = copy_board(_board)

        start, end = _action
        updated_board = update_board(_prev_board, copy_board(_board), start, end, _player_num)

        return ChessVNState(_board, updated_board, _player_num)

    def move(self, action: tuple[tuple[int], tuple[int]]):
        # This method will change value in _board
        _board = copy.deepcopy(self.board)

        start, end = action

        updated_board = update_board(self.prev_board, copy.deepcopy(_board), start, end, self.player_num)

        return VnChessState(_board, updated_board, -self.player_num)
