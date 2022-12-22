from utils import *
#Get possible moves from current state:

def check_move_valid(board, move, player):
    x1, y1 = move['pos']
    if  not (0<= x1<len(board)) or not (0<=y1<len(board)) or board[x1][y1] != player:
        # print("invail move", x1, y1)
        # print_board(board)
        return False
    action = move['move']
    x2, y2 = blind_move((x1, y1), action)
    if not (0<= x2 <len(board)) or not (0<=y2<len(board)) or board[x2][y2] != 0:
        # print("invail move2", x2, y2)
        # print_board(board)
        return False
    return True
    
#move valid move of player and return new board
def move_chess(board, move, player):
    xx, yy = move['pos']
    x, y = blind_move(move['pos'], move['move'])
    board[x][y] = player
    board[xx][yy] = 0

def get_valid_actions(board, player):
    # trap_informs = get_traps(board)
    trap_inform = get_pos_action_traps(board, player)
    if len(trap_inform) != 0:
        return trap_inform
    w, h = len(board), len(board[0])
    res = []
    for i in range(w):
        for j in range(h):
            if get_at(board,(i,j)) == player:
                actions = get_actions_of_chessman(board, (i,j))
                res += [
                    {
                    'pos': (i,j),
                    'move': action 
                    } for action in actions
                ]
    if len(res) == 0:
        print("can;t get action")
        print_board(board)
        exit()
    return res


def get_pos_action_traps(board, player_num) -> list[tuple[int, int], Action]:
    # TODO: Exact trap from last move of opponent
    '''
    Params:
        board: current board state
        active_pos: current position of last player moved chess
        player_num: player_num of next move player
    Returns:
        list((start_pos), action)
    '''
    # Result shape [(start_pos, action)]
    traps = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                continue
            is_possible_trap = False

            for sub_action in Action.get_half_actions():
                pos_1, pos_2 = blind_move((i,j), sub_action), \
                            blind_move((i,j), sub_action.get_opposite())
                num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)
                if num_1 == -player_num and num_2 == -player_num:
                    is_possible_trap = True
                    break
            if not is_possible_trap:
                continue
            pos_actions = []

            for sub_action in get_avail_actions((i,j)):
                pos_1, pos_2 = blind_move((i,j), sub_action), blind_move((i,j), sub_action.get_opposite())
                num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)

                if num_1 == player_num:
                    pos_actions.append({
                        'pos': pos_1,
                        'move': sub_action.get_opposite()
                    })
                if num_2 == player_num:
                    pos_actions.append({
                        'pos': pos_2,
                        'move': sub_action
                    })
            if len(pos_actions) != 0:
                traps += pos_actions
    return traps
