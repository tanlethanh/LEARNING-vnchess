from monte_nodes import *
from monte_chess_state import *
from monte import *

class MonteABState(AbstractGameState):
    def __init__(self, parent_state = None, state = None, player = 1, alpha = -10000, beta = 10000, mo = 0, vay = 0, ganh = 0):
        self.prev_board = parent_state
        self.board = state
        self.player = player
        self.alpha = alpha
        self.beta = beta
        self.mo = mo
        self.vay = vay
        self.ganh = ganh

    @property
    def game_result(self) -> int:
        value = (np.sum(np.array(self.board)))
        if value == 16:
            return 2
        elif value == -16:
            return -2
        elif value > 10:
            return 1
        elif value < -10:
            return -1
        else:
            return 0

    def is_game_over(self) -> bool:
        x = np.sum(np.array(self.board))
        return x == 16 or x == -16


    def move(self, move):
        # transform state to new state by trigger move,
        '''
        params:
            move:{
                'pos':tuple(int, int),
                'move': Action
                }
        returns:
            new_state
        '''
        ganh = 0.
        vay = 0.
        mo = 0.
        _prevboard = copy_board(self.board)
        _board = copy_board(self.board)

        start, end = move
        i, j = start
        if _board[i][j] != self.player:
            print(_board[i][j])
            print(self.player)
            raise Exception("Start position is not valid")

        active_position, is_possibility_trap = False, False
        if self.prev_board is not None:
            active_position, is_possibility_trap = get_active_position(self.prev_board, _board, -self.player)

        # Get all actions of chessman list pair (start, action)
        chessman_actions = []
        if is_possibility_trap and active_position is not None:
            chessman_actions = get_traps(_board, active_position, self.player) #[(start, end)]

        if not is_possibility_trap or len(chessman_actions) == 0:
            # print("hh")
            actions = get_actions_of_chessman(_board, start)
            chessman_actions = [(start, blind_move(start, action)) for action in actions]

        # Check the _end point is from valid action
        is_valid = False
        for s, e in chessman_actions:
            if start == s and end == e:
                is_valid = True
                break
        if not is_valid:
            print(chessman_actions)
            if is_possibility_trap:
                print("trap")
            else:
                print("not trap")
            raise Exception(f"Action is not valid: {start} -> {end}")

        i, j = end
        _board[i][j] = self.player

        i, j = start
        _board[i][j] = 0

        # Ganh truoc, vay sau <- vi co truong hop co ca ganh va vay
        # cap nhat neu co ganh
        for action in Action.get_half_actions():
            i1, j1 = blind_move(end, action)
            i2, j2 = blind_move(end, action.get_opposite())

            if(is_valid_position((i1,j1)) and is_valid_position((i2,j2))):
                if _board[i1][j1] == _board[i2][j2] == -self.player:
                    # print(f"\tUpdate board: kill at {i1, j1} and {i2, j2}")
                    _board[i1][j1] = self.player
                    _board[i2][j2] = self.player
                    ganh += 2.
            # This blind move can go out of board
        mo = len(get_traps(_board, end, -self.player))
        # cap nhat neu co vay
        surround_teams = get_surrounded_chesses(_board, self.player)
        if len(surround_teams): 
            vay+=len(surround_teams)
            _board = surround(_board, surround_teams, self.player)

        return type(self)(_prevboard, _board, -self.player, alpha = self.alpha, beta = self.beta, mo = mo, vay = vay, ganh = ganh)
    
    def get_legal_actions(self):
        return get_all_actions(self.prev_board,self.board, self.player)

class MonteABNode(MonteCarloTreeSearchNode):
    def __init__(self, state, parent_action = None, parent = None):
        super().__init__(state, parent_action, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None
        self._value = 0

    def best_child(self, W=0.5):
        total_value = np.sum([c.value for c in self.children])
        choices_weights = [(c.q/(c.n + 1)) + np.sqrt((2* np.log(self.n)/(c.n + 1))) + W * c.value/(abs(total_value) +1) for c in self.children]
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
        return self._value/self.n*50.0 + (np.sum(self.state.board))*self.state.player/8.0

    @property
    def q(self):
        win = self._results[2*self.state.player]
        stronger = self._results[self.state.player]
        loss = self._results[-2*self.state.player]
        weaker = self._results[-self.state.player]
        res = (10*win-10*loss + stronger - weaker)/self.n
        return res

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

        
    def rollout(self, threshold=5, num_simulation = 10, alpha = -1000, beta = 1000):
        '''
            make simulation through node with alpha beta
            params: threshold: int
            returns: 
                end_node game result
        '''
        current_state = self.state
        _mo, _vay, _ganh = 0, 0, 0
        while (alpha < beta) and threshold > 0:
            if (len(current_state.get_legal_actions()) != 0):
                feasibleChilds = []
                state_children = []
                possible_moves = current_state.get_legal_actions()
                for action in possible_moves:
                    children_state= current_state.move(action)
                    state_children.append(children_state)
                for children in state_children:
                    assert(isinstance(children, MonteABState))
                    children.alpha = max(alpha,children.alpha)
                    children.beta = min(beta, children.beta)
                    if children.alpha < children.beta:
                        feasibleChilds.append(children)
                next_state = self.rollout_policy(feasibleChilds)
                index = -current_state.player
                threshold -= 1
                current_state = next_state
                _mo += current_state.mo * index
                _vay += current_state.vay * index
                _ganh += current_state.ganh * index
            if current_state.is_game_over():
                if current_state.player == 1:
                    alpha = current_state.game_result
                else:
                    beta = current_state.game_result
                current_state = self.state
                threshold = 5
                num_simulation -= 1
                continue
            elif current_state.player == 1:
                alpha = np.max([child.alpha for child in feasibleChilds])
                # beta = np.max([child.beta for child in feasibleChilds])
            elif self.state.player == -1:
                # alpha = np.min([child.alpha for child in feasibleChilds])
                beta = np.min([child.beta for child in feasibleChilds])
            # print("alpha: ", alpha, "beta: ", beta)
        # if alpha > beta:
        #     print("cutoff")
        x_op = len(get_all_actions(current_state.prev_board, current_state.board, 1))
        o_op = len(get_all_actions(current_state.prev_board, current_state.board, -1))

        return x_op, o_op, current_state.game_result, _mo, _vay, _ganh
    def backpropagate(self, reward):
        '''
        params:
            reward: game_result, num_ganh, num_vay, num_mo
        '''
        x_op, o_op, result, mo, vay, ganh = reward
        self._value += (0.5 * o_op - x_op if self.state.player == -1 else 0.5 * x_op -o_op) + self.state.player *(10 *vay + 2*ganh - 5*mo)/16.0
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent is not None:
            self.parent.backpropagate(reward)

class ChessVNMonteCarloTreeSearch(object):

    def __init__(self, node):
        '''
        params
        node: MonteTreeNode
        '''
        self.root = node

    # def best_action(self, simulations_number = None, total_simulation_seconds=None, c_param = 1.4):
    #     '''
    #     params:
    #     simulations_numbers: int
    #         threshold of simulations performed to get best move
    #     total_simulation_seconds: float
    #         threshold of time avail for algorithm has to run. unit: second
    #     returns:
    #         moves: chess.move
    #     '''
    #     if simulations_number is None:
    #         assert(total_simulation_seconds is not None)
    #         end_time = time.time() + total_simulation_seconds
    #         while time.time() <= end_time:
    # def rollout(self, threshold=5, num_simulation = 10, alpha = -1000, beta = 1000):
    #     '''
    #         make simulation through node with alpha beta
    #         params: threshold: int
    #         returns: 
    #             end_node game result
    #     '''
    #     current_state = self.state
    #     _mo, _vay, _ganh = 0, 0, 0
    #     while (alpha < beta) and threshold > 0:
    #         if (len(current_state.get_legal_actions()) != 0):
    #             feasibleChilds = []
    #             state_children = []
    #             possible_moves = current_state.get_legal_actions()
    #             for action in possible_moves:
    #                 children_state= current_state.move(action)
    #                 state_children.append(children_state)
    #             for children in state_children:
    #                 assert(isinstance(children, MonteABState))
    #                 children.alpha = max(alpha,children.alpha)
    #                 children.beta = min(beta, children.beta)
    #                 if children.alpha < children.beta:
    #                     feasibleChilds.append(children)
    #             next_state = self.rollout_policy(feasibleChilds)
    #             index = -current_state.player
    #             threshold -= 1
    #             current_state = next_state
    #             _mo += current_state.mo * index
    #             _vay += current_state.vay * index
    #             _ganh += current_state.ganh * index
    #         if num_simulation < 0:
    #             break
    #         if current_state.is_game_over():
    #             if current_state.player == 1:
    #                 alpha = current_state.game_result
    #             else:
    #                 beta = current_state.game_result
    #             current_state = self.state
    #             threshold = 5
    #             num_simulation -= 1
    #             continue
    #         elif current_state.player == 1:
    #             alpha = np.max([child.alpha for child in feasibleChilds])
    #             # beta = np.max([child.beta for child in feasibleChilds])
    #         elif self.state.player == -1:
    #             # alpha = np.min([child.alpha for child in feasibleChilds])
    #             beta = np.min([child.beta for child in feasibleChilds])
    #         # print("alpha: ", alpha, "beta: ", beta)
    #     # if alpha > beta:
    #     #     print("cutoff")
    #     x_op = len(get_all_actions(current_state.prev_board, current_state.board, 1))
    #     o_op = len(get_all_actions(current_state.prev_board, current_state.board, -1))

    #     return x_op, o_op, current_state.game_result, _mo, _vay, _ganh

    #             # print("Roll out")
    #             v = self._tree_policy()
    #             assert(isinstance(v,MonteABNode))
    #             reward = v.rollout(5)
    #             # v.backpropagate(reward, v.index)
    #             v.backpropagate(reward)
    #     return self.root.best_child()

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



def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    if _player == 1:
        _remain_time = _remain_time_x
    else:
        _remain_time = _remain_time_o

    initial_board_state = MonteABState(parent_state =_prev_board, state = _board, player=_player)
    root = MonteABNode(state=initial_board_state)
    engine = ChessVNMonteCarloTreeSearch(root)
    # duration = 100
    best_child = engine.best_action(total_simulation_seconds=3.0, c_param=0.2)
    best_move = best_child.parent_action
    start, end = best_move
    assert(isinstance(best_child, MonteABNode))
    print(f"\t MONTE move: {start} -> {end}")
    return (start, end)