from monte_carlo_tree_search import ChessVNMonteCarloTreeSearch
from monte_nodes import ChessVNNode
from monte_chess_state import ChessVNState
from game_manager import *
import numpy as np
player1 =  1
player2 = -1
state = [
    [ 1,  1,  1,  1,  1],
    [ 1,  0,  0,  0,  1],
    [ 1,  0,  0,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1, -1, -1, -1, -1]
    ]
initial_board_state =ChessVNState(state=state, next_to_move=player2)

root = ChessVNNode(state=initial_board_state)
# print(root)
print(initial_board_state)
mcts_engine = ChessVNMonteCarloTreeSearch(root)

print_board(state)
print("---"*20)
best_move = mcts_engine.best_action(simulations_number=10)

# print_board(best_node.parent.state.board)
print("---"*20)
print(best_move.parent_action)
# print_board(best_node.state.board)

# print(get_active_position(state, best_node.state.board, player2))