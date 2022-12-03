from action import Action
from utils import blind_move, get_at, get_avail_actions, blind_move, get_active_position, is_valid_position
import copy

class Chess:

    def __init__(self, board):
        pass
        

    def move_chess_man(self, start: tuple[int, int], action: Action) -> tuple[int, int]:
        """
        This method take a valid action for chess man, action must be checked.

        :param start: position of chosen chess man
        :param action: Action
        :return: end position
        """
        # TODO:
        return blind_move(start,action)
        
    def is_valid_position(self,board, pos: tuple[int, int], num_player) -> bool:
        x, y = pos
        return board[x][y] == num_player

    def get_valid_actions(self,board, position: tuple[int, int]) -> list[Action]:
        """
        This method return list of all valid actions from a position in the game board
        (don't care about chess man, just position).

        :param position: a position, tuple (x, y)
        :return: list of all valid actions
        """
        actions = []
        
        x, y = position
        for i in range(x-1,x+1):
            for j in range(y-1, y+1):
                if (not is_valid_position((i,j)) or (x == i and j == y) ):
                    continue 
                if (board[i,j] == 0):
                    actions.append(Action((i - x, j - y)))
        return actions

    def update_board(self, board: list[list[int]], start: tuple[int, int], action: Action, player_num: int) -> list[list[int]]:
        # TODO: Di chuyen quan co cua minh
        end = self.move_chess_man(start=start,action=action)
        x, y = start
        new_x, new_y = end
        board[new_x][new_y] = board[x][y]
        board[x][y] = 0

        # TODO: Lay cac cum co bi vay
        surrounded_teams = self.get_surrounded_chesses(board, player_num)
        
        # TODO: Bien co vay thanh co cua minh
        board = self.surround(board, surrounded_teams)
        return board
    
    def get_surrounded_chesses(self, board, player_num):
        current_board = copy.deepcopy(board)

        w, h = len(current_board), len(current_board[0])
        teams = []
        for i in range(w):
            for j in range(h):
                if current_board[i][j] == -player_num:
                    team  = []
                    explore = []
                    team.append((i,j))
                    explore.append((i,j))
                    is_surrounded = True
                    while len(explore) != 0:
                        curr_x, curr_y = explore.pop()
                        moves = get_avail_actions((curr_x, curr_y))
                        for move in moves:
                            next_x, next_y = blind_move((curr_x, curr_y), move)
                            if(is_valid_position((next_x,next_y)) and current_board[next_x][next_y] != 2):
                                if current_board[next_x][next_y] == 0:
                                    is_surrounded = False
                                elif current_board[next_x][next_y] == -player_num:
                                    team.append((next_x,next_y))
                                    explore.append((next_x,next_y))
                        current_board[curr_x][curr_y] = 2
                    current_board[i][j] = 2
                                
                    if is_surrounded:
                        teams.append(team)

        return teams

    def surround(self, board, surrounded_teams):
        for team in surrounded_teams:
            for chess_index in team:
                x, y  = chess_index
                board[x][y] *= -1
        return board
            



def move_in_board(board: list[list[int]], index: tuple[int, int], action: Action) \
        -> tuple[tuple[int, int], tuple[int, int]]:
    # TODO
    pass


def get_traps(board, active_pos, player_num) -> list[tuple[tuple[int, int], Action]]:
    # TODO: Exact trap from last move of opponent
    traps = []
    for action in list(Action):
        adjacent_pos = blind_move(active_pos, action)
        adjacent_num = get_at(board, adjacent_pos)

        if adjacent_num == 0:
            starts = []
            is_trap = False

            for sub_action in Action.get_positive_action():
                pos_1, pos_2 = blind_move(adjacent_pos, sub_action), \
                               blind_move(adjacent_pos, sub_action.get_opposite())
                num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)

                if num_1 == -player_num and num_2 == -player_num:
                    is_trap = True

                if num_1 == player_num:
                    starts.append(pos_1)
                if num_2 == player_num:
                    starts.append(pos_2)

            if is_trap and len(starts) > 0:
                traps += [(start, adjacent_pos) for start in starts]

    return traps


def get_all_valid_actions(board, player):
    pass


def choose_action(prev_board, board, player, all_actions):
    pass


def move(prev_board, board, player, remain_time_x, remain_time_o):
    player_num = 1 if player == "X" else -1
    active_position, is_possibility_trap = get_active_position(prev_board, board, player_num)
    all_actions = get_traps(board, active_position, player_num) \
        if is_possibility_trap else get_all_valid_actions(board, player)
    return choose_action(prev_board, board, player, all_actions)
