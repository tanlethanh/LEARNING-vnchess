
class MonteAgent():
    def __init__(self, prev_state, state, player, remain_move = None, remain_duration = None, level= 'medium'):
        np.random.seed(1234)
        self.level = level
        self.remain_move = remain_move
        self.remain_duration = remain_duration
        # parent_move = get_last_move(prev_state, state, -player)
        self.initial_board_state = ChessVNState(parent_state = prev_state, state = state, next_to_move=player)
        self.root = ChessVNNode(state=self.initial_board_state)
        self.engine = ChessVNMonteCarloTreeSearch(self.root)
        self.duration = 100
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
            return self.engine.best_action(simulations_number=100, c_param=0.2)
            if self.remain_duration/self.duration > 0.95:
                # print("beginging")
                return self.engine.best_action(simulations_number=50, c_param=0.2, deep_threshold=5)
            elif self.remain_duration/self.duration > 0.8:
                # print("beginging")
                return self.engine.best_action(simulations_number=100, c_param=0.15, deep_threshold=10)
            elif self.remain_duration/self.duration > 0.7:
                # print("sau begin")
                return self.engine.best_action(simulations_number=100, c_param=0.1, deep_threshold=5)
            elif self.remain_duration/self.duration > 0.4:
                # print("sap end")
                return self.engine.best_action(simulations_number=300, c_param=0.5, deep_threshold=3)
            else:
                # print("endgame")
                return self.engine.best_action(simulations_number=300, c_param=0, deep_threshold=3)