from game_manager import *
import numpy as np
from monte_utils import *
class AbstractGameState():
    def game_result(self) -> int:
        '''
        return:
            1 if player 1 win
            0 if unknow
            -1 if player 2 win
        '''
        pass

    def is_game_over(self) -> bool:
        '''
        return boolean indicating if the game is over
        '''
        pass

    def move(self, action):
        '''
        perform action and return resulting state

        action: abstract action
        return:
        abstract state
        '''
        pass

    def get_legal_actions(self):
        '''
        get possible action can perform at current game state
        return:
        [action]
        '''
        pass

class ChessVNState(AbstractGameState):
    #next to move: next player
    def __init__(self, state = None, parent_move = None,  next_to_move=1):
        '''
        state: chess board
        '''
        self.board = state
        self.prev_move = parent_move
        self.board_size = np.array(state).shape[0]
        self.next_to_move = next_to_move
    
    # def __str__(self) -> str:
    #     res = "Next to move: " + str(self.next_to_move)
    #     res += '\n'.join(','.join(row) for row in self.board)
    #     return res

    @property
    def game_result(self) -> int:
        x_op = len(get_valid_actions(self.prev_move, self.board, 1))
        o_op = len(get_valid_actions(self.prev_move, self.board,-1))
        value = (np.sum(np.array(self.board)))
        if value == 16 or value == -16:
            return value / 2
        return (value + (x_op - o_op)) / 16
        # return np.sum(np.array(self.board)) > 0 ? 1: 1

    def is_game_over(self) -> bool:
        x = np.sum(np.array(self.board))
        return x == 16 or x == -16

    def is_move_legal(self, move):
        return check_move_valid(self.board, move, player=self.next_to_move)

    def move(self, move):
        if not self.is_move_legal(move):
            raise Exception("move{0} on board{1} is not legal".format(move, self.board))
        new_board = copy_board(self.board)
        init_x, init_y = move['pos']
        x, y = blind_move(move['pos'], move['move'])
        new_board[x][y] = new_board[init_x][init_y]
        new_board[init_x][init_y] = 0
        for action in Action.get_half_actions():
            pos1, pos2 = blind_move((x,y),action), blind_move((x,y), action.get_opposite())
            if not (is_valid_position(pos1) and is_valid_position(pos2)):
                continue
            num_1, num_2 = get_at(new_board, pos1), get_at(new_board, pos2)
            if num_1 == num_2 == -new_board[x][y]:
                # print('ganh at', pos1, pos2, self.next_to_move)
                new_board[pos1[0]][pos1[1]] = new_board[x][y]
                new_board[pos2[0]][pos2[1]] = new_board[x][y]
        
        surround_teams = get_surrounded_chesses(new_board, self.next_to_move)

        if len(surround_teams) != 0:
            new_board = surround(new_board, surround_teams, self.next_to_move)
        next_to_move = - self.next_to_move
        return type(self) (new_board, move, next_to_move)
    
    def get_legal_actions(self):
        return get_valid_actions(self.prev_move, self.board, self.next_to_move)