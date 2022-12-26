from monte_nodes import *
from monte_chess_state import *
from monte_utils import *

class MonteABState(AbstractGameState):
    def __init__(self, parent_state = None, state = None, player = 1, alpha = -10000, beta = 10000):
        self.prev_board = parent_state
        self.board = state
        self.player = player
        self.alpha = alpha
        self.beta = beta

    @property
    def game_result(self) -> int:
        value = (np.sum(np.array(self.board)))
        if value < 14:
            return 1
        elif value < -14:
            return -1
        else:
            return 0

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

class MonteABNode(MonteCarloTreeSearchNode):
    def __init__(self, state, parent_action = None, parent = None):
        super().__init__(self, state, parent_action, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None
    
    def best_child(self, W, Pmc):
        choices_weights = [(c.q/c.n) + np.sqrt((2* np.log(self.n)/c.n)) + W*Pmc/(c.n + 1) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            actions = self.state.get_legal_actions()
            np.random.shuffle(actions)
            self._untried_actions = actions
        return self._untried_actions
    
    @property
    def value(self):
        pass

    @property
    def q(self):
        win = self._results[self.state.player]
        loss = self._results[-self.state.player]
        return win-loss

    @property
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self.untried_actions.pop()
        next_state= self.state.move(action)
        child_node = MonteABNode(next_state, parent_action=action, parent= self)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout_policty(self, possibleChilds):
        '''
        Apply rollout policy to choose node with max uct score.
        return:
            MonteABNode
        '''
        return possibleChilds[np.random.randint(len(possibleChilds))]

        
    def rollout(self):
        '''
            make simulation through node with alpha beta
            params: threshold: int
            returns: 
                end_node game result
        '''
        current_state = self.state
        alpha, beta = -1000, 1000
        while (alpha < beta) and not(current_state.is_game_over()):
            if (len(self.untried_actions) != 0):
                feasibleChilds = []
                state_children = []
                possible_moves = current_state.get_legal_actions()
                for action in possible_moves:
                    children_state = current_state.move(action)
                    state_children.append(children_state)
                    pass
                for children in state_children:
                    assert(isinstance(children, MonteABNode))
                    children.alpha = max(alpha,children.alpha)
                    children.beta = min(beta, children.beta)
                    if children.alpha < children.beta:
                        feasibleChilds.append(children)
                next_state = self.rollout_policy(feasibleChilds)
                current_state = next_state.alphaBetaRollout(next_state.v_p, next_state.v_m)
            if current_state.is_game_over():
                alpha = current_state.game_results
                beta = current_state.game_results
                return current_state.result
            elif current_state.player == 1:
                alpha = np.max([child.alpha for child in feasibleChilds])
                beta = np.max([child.beta for child in feasibleChilds])
            elif self.state.player == -1:
                alpha = np.min([child.alpha for child in feasibleChilds])
                beta = np.min([child.beta for child in feasibleChilds])

    def backpropagate(self, reward):
        '''
        params:
            reward: game_result, num_ganh, num_vay, num_mo
        '''
        pass