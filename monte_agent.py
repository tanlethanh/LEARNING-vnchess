from monte_carlo_tree_search import ChessVNMonteCarloTreeSearch
from monte_nodes import ChessVNNode
from monte_chess_state import ChessVNState
from game_manager import *
from monte_utils import *
import numpy as np

state = [
    [ 1,  1,  0,  1,  1],
    [ 1,  0,  1,  0,  1],
    [ 1, -1, -1,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1,  0,  0, -1, -1]
    ]

class MonteAgent():
    def __init__(self,prev_state, state, player, remain_move = None, remain_duration = None, level= 'easy'):
        np.random.seed(1234)
        self.level = level
        self.remain_move = remain_move
        self.remain_duration = remain_duration
        parent_move = get_last_move(prev_state, state, -player)
        self.initial_board_state = ChessVNState( state = state, parent_move=parent_move, next_to_move=player)
        self.root = ChessVNNode(state=self.initial_board_state)
        self.engine = ChessVNMonteCarloTreeSearch(self.root)
        self.duration = 50
    def move(self):
        if self.level == 'easy':
            return self.engine.best_action(simulations_number=20, c_param=np.random.randint(0, 20)/5, deep_threshold=np.random.randint(1,2))
        if self.level == 'medium':
            if self.remain_duration/self.duration > 0.8:
                return self.engine.best_action(simulations_number=50, c_param=self.remain_duration/self.duration, deep_threshold=5)
            elif self.remain_duration/self.duration > 0.5:
                return self.engine.best_action(simulations_number=100, c_param=self.remain_duration/self.duration, deep_threshold=10)
            else:
                return self.engine.best_action(simulations_number=500, c_param=self.remain_duration/self.duration, deep_threshold=20)
        if self.level == 'expert':
            if self.remain_duration/self.duration > 0.8:
                return self.engine.best_action(simulations_number=300, c_param=2., deep_threshold=3)
            elif self.remain_duration/self.duration > 0.7:
                return self.engine.best_action(simulations_number=300, c_param=3., deep_threshold=3)
            elif self.remain_duration/self.duration > 0.4:
                return self.engine.best_action(simulations_number=300, c_param=2., deep_threshold=4)
            else:
                return self.engine.best_action(simulations_number=300, c_param=0, deep_threshold=3)