from game_manager import *
import numpy as np
# from monte_utils import *
import monte_nodes
from monte_carlo_tree_search import *

import time
np.random.seed(int(time.time()))
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
    def __init__(self, parent_state = None, state = None, next_to_move=1):
        '''
        state: chess board
        '''
        self.prev_board = parent_state
        self.board = state
        self.board_size = np.array(state).shape[0]
        self.next_to_move = next_to_move
        # self.prev_move = parent_move
    
    # def __str__(self) -> str:
    #     res = "Next to move: " + str(self.next_to_move)
    #     res += '\n'.join(','.join(row) for row in self.board)
    #     return res

    @property
    def game_result(self) -> int:
        # x_op = len(get_avail_valid_actions( self.board, 1))
        # o_op = len(get_avail_valid_actions( self.board,-1))
        value = (np.sum(np.array(self.board)))
        if value < 14:
            return 2
        elif value < -14:
            return 0
        else:
            return 1
        # if value == 16 or value == -16:
        #     return 1000
        # return value 
        # return (value + (x_op - o_op))
        # return np.sum(np.array(self.board)) > 0 ? 1: 1

    def is_game_over(self) -> bool:
        x = np.sum(np.array(self.board))
        return x == 16 or x == -16

    def is_move_legal(self, move):
        return check_move_valid(self.board, move, player=self.next_to_move)

    def move(self, move):
        # transform state to new state by trigger move,
        '''
        params:
            move:{
                'pos':tuple(int, int),
                'move': Action
                }
        returns:
            new_state, num_ganh, num_vay, num_mo
        '''
        ganh = 0
        vay = 0
        mo = 0
        assert(move is not None)
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
                ganh += 1

        surround_teams = get_surrounded_chesses(new_board, self.next_to_move)

        if len(surround_teams) != 0:
            new_board = surround(new_board, surround_teams, self.next_to_move)
            vay += len(surround_teams)
        mo = len(get_pos_action_traps(board= new_board, prev_move=move, player_num= -self.next_to_move))
        return type(self) (copy_board(self.board), new_board, -self.next_to_move), ganh, vay, mo
    
    def get_legal_actions(self):
        return get_valid_actions(self.prev_board, self.board, self.next_to_move)


if __name__ == "__main__":
    prev_board = [
        [ 1,  1,  0,  1,  1],
        [ 1,  0,  1,  1,  1],
        [-1, -1,  0,  0,  1],
        [ 0, -1,  0, -1,  1],
        [-1, -1,  0,  0,  0],
    ]
    board = [
        [ 1,  1,  0,  1,  1],
        [ 1,  0,  1,  1,  1],
        [-1, -1,  0,  0,  1],
        [ 0, -1,  0, -1,  0],
        [-1, -1,  0,  0,  1],
    ]
    state = ChessVNState(prev_board, board, next_to_move=-1)
    node = monte_nodes.ChessVNNode(state=state)
    search = ChessVNMonteCarloTreeSearch(node)
    last_move = get_last_move(prev_board,board, 1)
    pos2 = blind_move(last_move['pos'], last_move['move'])
    # print(pos2)
    # print(get_pos_action_traps(get_last_move(prev_board, board, 1),board,-1))
    # print(get_valid_actions(prev_board, board, -1))
    print(state.get_legal_actions())
    # print(node.untried_actions)
    
    # actions = search.best_action(simulations_number=1000, c_param=6., deep_threshold=5).parent_action
    # print(actions)
    # new_board = update_board(prev_board,board,actions['pos'], blind_move(actions['pos'],actions['move']), -1)
    # print_board(new_board)
    # for i in range(1):
    # print_board(prev_board)
    # print("---"*20)
    # print_board(search.root.state.board)
    # print("---"*20)
    # v = search._tree_policy()
    # reward = v.rollout(threshold=2)
    # v.backpropagate( reward, v.index)
    # # print("----"*20)
    # # print_board(v.state.board)
    # print("----"*20)
    # print(reward[3],reward[1],reward[2])
    