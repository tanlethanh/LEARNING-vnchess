import numpy as np
from collections import defaultdict
from monte_chess_state import *
from game_manager import *
import time
np.random.seed(int(time.time()))
class MonteCarloTreeSearchNode():
    def __init__(self, state, parent_action = None, parent = None):
        '''
        Params: state: monte_carlo_board_state
        parent: node
        '''
        np.random.seed(int(time.time()))
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []

    def __str__(self) -> str:
        return "State: " + str(self.state.board) + "\nAction: " + str(self.parent_action)

    @property
    def untried_actions(self):
        pass

    @property
    def q(self):
        pass
    
    @property
    def n(self):
        pass

    @property
    def expand(self):
        pass

    @property
    def is_terminal_node(self): #check if leaf node
        pass

    def rollout(self):
        pass

    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param = 1.4):
        # exit()
        choices_weights = [
            float(c.q)/float(c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        # if len(choices_weights) == 0:
        #     print()
        #     exit()
        return self.children[np.argmax(choices_weights)] #return child with greatest promise value

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    
class ChessVNNode(MonteCarloTreeSearchNode):
    # def __init__(self, state, parent_action = None, parent=None, index = None):

    def __init__(self, state, parent_action = None, parent=None):
        super().__init__( state, parent_action, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        # self.index = index
        self._untried_actions = None
        self._vay = defaultdict(int)
        self._ganh = defaultdict(int)
        self._mo = defaultdict(int)

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            actions = self.state.get_legal_actions()
            np.random.shuffle(actions)
            self._untried_actions = actions
        return self._untried_actions

    
    @property
    def q(self):
        # wins = np.sum(self._results)
        # [self.parent.state.next_to_move]
        # loses = self._results[-1 * self.parent.state.next_to_move]
        # res = 0
        # q_res_array = np.array(list(self._results))
        # q_res = np.sum(q_res_array/(np.max(q_res_array,initial=1.0)))
        # listaction = [float(len(get_avail_valid_actions(c.state.board, -c.state.next_to_move))) for c in self.children]
        # q_action = np.array(listaction)
        # q_action = np.sum(q_action)/(np.max(q_action,initial=1.0))
        # q_vay_array = np.array(list(self._vay))
        # q_vay = np.sum(q_vay_array/(np.max(q_vay_array,initial=1.0) ))
        # # q_ganh_array = np.array(list(self._ganh))
        # # q_ganh = np.sum(q_ganh_array/(np.max(q_ganh_array, initial=1.0)))
        # q_mo_array = np.array(list(self._mo))
        # q_mo = np.sum(q_mo_array/(np.max(q_mo_array, initial=1.0) ))
        # res = 4.0 * float(q_res) - 0.5 * float(q_mo) + 1.*float(q_vay) + len(get_avail_valid_actions(self.state.board, self.state.next_to_move))/(len(get_avail_valid_actions(self.state.board, self.state.next_to_move)) + 1)
        win_index = 1 + self.state.next_to_move
        win = self._results[win_index]
        loss = self._results[2 - win_index]
        return win-loss
        # return res + q_action/2
        # return np.sum(np.array(list(self._results)))
        # - loses
    
    @property
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self.untried_actions.pop()
        next_state, _, _, _ = self.state.move(action)
        # child_index = len(self.children)
        # child_node = ChessVNNode(next_state, parent_action=action, parent= self, index= child_index)
        child_node = ChessVNNode(next_state, parent_action=action, parent= self)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def rollout(self):
        '''
            make simulation through node with depth threshold
            params: threshold: int
            returns: 
                end_node game result, num of _ganh, _vay, _mo make by this node player
        '''
        current_rollout_state = self.state
        # print(current_rollout_state)
        _ganh, _vay, _mo = 0, 0, 0
        # print("----"*20 )
        # print("Before roll out")
        # print_board(current_rollout_state.board)
        # print( _ganh, _vay, _mo)
        while not (current_rollout_state.is_game_over()) :
            possible_moves = current_rollout_state.get_legal_actions()
            player = current_rollout_state.next_to_move
            action = self.rollout_policy(possible_moves)
            current_rollout_state, ganh, vay, mo = current_rollout_state.move(action)
            _ganh += ganh * player
            _vay += vay * player
            _mo += mo * player
            # print("----"*20 )
            # print("Rolling: ", player)
            # print("Take Action: ", action)
            # print_board(current_rollout_state.board)
            # print( _ganh, _vay, _mo)
            # print("----"*20 )
        # print("----"*20 )
        # print("After rollout")
        # print_board(current_rollout_state.board)
        # print( _ganh, _vay, _mo)
        # print("----"*20 )
        # time.sleep(100)
        return current_rollout_state.game_result, _ganh, _vay, _mo

    # def backpropagate(self, reward, index):
    def backpropagate(self, reward):
        '''
        params:
            reward: game_result, num_ganh, num_vay, num_mo
        '''
        # assert(index is not None)
        game_result, ganh, vay, mo = reward
        # self._ganh[index] += ganh  * self.state.next_to_move
        # self._vay[index] += vay * self.state.next_to_move
        # self._mo[index] += mo * self.state.next_to_move
        # self._results[index] += game_result * self.state.next_to_move
        self._results[game_result] += 1.
        self._number_of_visits += 1.
        if self.parent is not None:
            assert(isinstance(self.parent, ChessVNNode))
            # self.parent.backpropagate(reward, self.index)
            self.parent.backpropagate(reward)



if __name__ == "__main__":
    from monte_chess_state import *
    prev_board = [
        [ 0,  0,  1,  1,  1],
        [ 1, -1,  0, -1,  0],
        [ 0,  0, -1, -1, -1],
        [ 1, -1, -1,  0, -1],
        [ 1,  1, -1,  0,  0],
    ]
    board = [
        [ 0,  1,  0,  1,  1],
        [ 1, -1,  0, -1,  0],
        [ 0,  0, -1, -1, -1],
        [ 1, -1, -1,  0, -1],
        [ 1,  1, -1,  0,  0],
    ]
    # state = ChessVNState(prev_board, board, next_to_move=-1)
    # node = ChessVNNode(state=state)
    # search = ChessVNMonteCarloTreeSearch(node)
    # x = node.untried_actions.pop()
    # print(node.expand())
    # print(x)
    # print(node.state)