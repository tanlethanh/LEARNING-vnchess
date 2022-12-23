import numpy as np
from collections import defaultdict
from monte_chess_state import *
from game_manager import *

class MonteCarloTreeSearchNode():
    def __init__(self, state,parent_action = None, parent = None):
        '''
        Params: state: monte_carlo_board_state
        parent: node
        '''
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
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)] #return child with greatest promise value

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    
class ChessVNNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent_action = None, parent=None):
        super().__init__( state, parent_action, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        # self._results = []
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        # wins = np.sum(self._results)
        # [self.parent.state.next_to_move]
        # loses = self._results[-1 * self.parent.state.next_to_move]
        res = 0
        for i in self._results:
            res += self._results[i]
        return res 
        # - loses
    
    @property
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = ChessVNNode(next_state, parent_action=action, parent= self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def rollout(self, threshold = 100):
        current_rollout_state = self.state
        assert(isinstance(current_rollout_state, ChessVNState))
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
            threshold -=1
            if threshold < 0:
                break
        return current_rollout_state.game_result
    
    def backpropagate(self, reward):

        self._results[self._number_of_visits] += reward * self.state.next_to_move
        self._number_of_visits += 1.
        if self.parent is not None:
            self.parent.backpropagate(reward)