import time
from collections import defaultdict
import numpy as np

from game_state import VnChessState


class ChessVNMonteCarloTreeSearch(object):

    def __init__(self, node):
        '''
        params
        node: MonteTreeNode
        '''
        self.root = node

    def best_action(self, simulations_number=None, total_simulation_seconds=None, c_param=1.4, deep_threshold=100):
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
            assert (total_simulation_seconds is not None)
            end_time = time.time() + total_simulation_seconds
            while time.time() <= end_time:
                v = self._tree_policy()
                reward = v.rollout(deep_threshold)
                v.backpropagate(reward)

        else:
            for _ in range(0, simulations_number):
                v = self._tree_policy()
                reward = v.rollout(deep_threshold)
                v.backpropagate(reward)

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


# DONE
class MonteCarloTreeSearchNode:

    def __init__(self, state, parent_action=None, parent=None):
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
    def is_terminal_node(self):  # check if leaf node
        pass

    def rollout(self):
        pass

    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            float(c.q) / float(c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]


class ChessVNNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent_action=None, parent=None):
        super().__init__(state, parent_action, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            actions = self.state.get_all_legal_actions()
            np.random.shuffle(actions)
            self._untried_actions = actions
        return self._untried_actions

    @property
    def q(self):
        win_index = 1 + self.state.player_num
        win = self._results[win_index]
        loss = self._results[2 - win_index]
        return win - loss

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = ChessVNNode(next_state, parent_action=action, parent=self)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self, threshold=100):
        '''
            make simulation through node with depth threshold
            params: threshold: int
            returns:
                end_node game result
        '''
        current_rollout_state = self.state

        while not (current_rollout_state.is_game_over()):
            possible_moves = current_rollout_state.get_all_legal_actions()
            player = current_rollout_state.player_num
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
            threshold -= 1
            if threshold < 0:
                break

        return current_rollout_state.game_result

    def backpropagate(self, reward):
        '''
        params:
            reward: game_result
        '''
        game_result = reward
        self._results[game_result] += 1.
        self._number_of_visits += 1.
        if self.parent is not None:
            assert (isinstance(self.parent, ChessVNNode))
            self.parent.backpropagate(reward)


class MonteAgent:

    def __init__(self, prev_state, state, player, remain_move=None, remain_duration=None, level='medium'):
        np.random.seed(1234)
        self.level = level
        self.remain_move = remain_move
        self.remain_duration = remain_duration

        self.initial_board_state = VnChessState(prev_board=prev_state, board=state, player_num=player)
        self.root = ChessVNNode(state=self.initial_board_state)
        self.engine = ChessVNMonteCarloTreeSearch(self.root)
        self.duration = 100

    def move(self):
        if self.level == 'easy':
            return self.engine.best_action(simulations_number=20, c_param=np.random.randint(0, 20) / 5,
                                           deep_threshold=np.random.randint(1, 2))
        if self.level == 'medium':
            if self.remain_duration / self.duration > 0.8:
                return self.engine.best_action(simulations_number=50, c_param=self.remain_duration / self.duration,
                                               deep_threshold=5)
            elif self.remain_duration / self.duration > 0.5:
                return self.engine.best_action(simulations_number=100, c_param=self.remain_duration / self.duration,
                                               deep_threshold=10)
            else:
                return self.engine.best_action(simulations_number=500, c_param=self.remain_duration / self.duration,
                                               deep_threshold=20)
        if self.level == 'expert':
            return self.engine.best_action(simulations_number=500, c_param=0.2,
                                           deep_threshold=np.random.randint(50, 100))


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    if _player == 1:
        _remain_time = _remain_time_x
    else:
        _remain_time = _remain_time_o

    monte = MonteAgent(_prev_board, _board, _player, remain_duration=_remain_time, level='easy')

    best_child = monte.move()
    start, end = best_child.parent_action

    assert (isinstance(best_child, ChessVNNode))

    print(f"\t MONTE move: {start} -> {end}")
    return start, end
