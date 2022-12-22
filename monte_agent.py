from monte_carlo_tree_search import ChessVNMonteCarloTreeSearch
from monte_nodes import ChessVNNode
from monte_chess_state import ChessVNState
from game_manager import *
import numpy as np



state = [
    [ 1,  1,  0,  1,  1],
    [ 1,  0,  1,  0,  1],
    [ 1, -1, -1,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1,  0,  0, -1, -1]
    ]

class MonteAgent():
    def __init__(self, state, player, simulations_number = None, simulation_second = None):
        self.initial_board_state = ChessVNState(state=state, next_to_move=player)
        self.root = ChessVNNode(state=self.initial_board_state)
        self.engine = ChessVNMonteCarloTreeSearch(self.root)
    def move(self):
        return self.engine.best_action(simulations_number=50)