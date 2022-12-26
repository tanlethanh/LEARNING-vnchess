import time
from monte_nodes import *

class ChessVNMonteCarloTreeSearch(object):

    def __init__(self, node):
        '''
        params
        node: MonteTreeNode
        '''
        self.root = node

    def best_action(self, simulations_number = None, total_simulation_seconds=None, c_param = 1.4):
        '''
        params:
        simulations_numbers: int
            threshold of simulations performed to get best move
        total_simulation_seconds: float
            threshold of time avail for algorithm has to run. unit: second
        returns:
            moves: chess.move
        '''
        if simulations_number is None:
            assert(total_simulation_seconds is not None)
            end_time = time.time() + total_simulation_seconds
            while time.time() <= end_time:
                v = self._tree_policy()
                reward = v.rollout()
                # v.backpropagate(reward, v.index)
                v.backpropagate(reward)

        else:
            for _ in range(0, simulations_number):
                v = self._tree_policy()
                reward = v.rollout()
                v.backpropagate(reward)
                # v.backpropagate(reward, v.index)

        return self.root.best_child(c_param=c_param)

    def _tree_policy(self):
        '''
        selects node to run rollout/playout for
        '''
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

