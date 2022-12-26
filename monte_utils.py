from utils import *
from game_manager import get_actions_of_chessman
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

def get_valid_actions(prev_board, board, player):
    # trap_informs = get_traps(board)

    w, h = len(board), len(board[0])
    if prev_board is not None:
        open_move_flag = True
        for i in range(h):
            for j in range(w):
                if board[i][j] == -player and prev_board[i][j] == player:
                    open_move_flag = False
        
        if open_move_flag:
            # print("open")
            assert(prev_board is not None and board is not None)
            prev_move = get_last_move(prev_board, board, -player)
            assert(prev_move is not None)
            trap_inform = get_pos_action_traps(prev_move, board, player)
            if len(trap_inform) != 0:
                return trap_inform
    return get_avail_valid_actions(board, player)

def get_avail_valid_actions(board, player):
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
    return res

def get_pos_action_traps(prev_move, board, player_num) -> list[tuple[int, int], Action]:
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
    if prev_move is None:
        return traps
    op_pos = blind_move(prev_move['pos'], prev_move['move'])
    # print(op_pos)
    # print('current_pos', op_pos)
    for adj_action in get_avail_actions(op_pos):
        adj_pos = blind_move(op_pos, adj_action)
        adj_num = get_at(board, adj_pos)
        if adj_num != 0:
            continue
        # print(adj_pos)
        next_op_pos = blind_move(adj_pos, adj_action)
        if get_at(board, next_op_pos) != get_at(board, op_pos):
            # print(next_op_pos)
            continue
        # print("posible trap pos: ", adj_pos)
        # print("Next pos: ", next_op_pos)
        for action in get_avail_actions(adj_pos):
            pos_pos = blind_move(adj_pos, action)
            num = get_at(board, pos_pos)
            if num == player_num:
                # print("added", pos_pos, action.get_opposite())
                traps.append({
                    'pos': pos_pos,
                    'move': action.get_opposite()
                })
        # for action in get_avail_half_actions(adj_pos):
        #     pos_1, pos_2 = blind_move(adj_pos, action), blind_move(adj_pos, action.get_opposite())
        #     num_1, num_2 = get_at(board, pos_1), get_at(board, pos_2)
        #     print("2 oposite pos: ", pos_1, pos_2, num_1, num_2)
        #     if num_1 == player_num:
        #         # print(pos_1)
        #         # print(action.get_opposite())
        #         traps.append({
        #             'pos': pos_1,
        #             'move': action.get_opposite()
        #         })
        #     if num_2 == player_num:
        #         # print(pos_2)
        #         # print(action)
        #         traps.append({
        #             'pos': pos_2,
        #             'move': action
        #         })
    # print(len(traps))
    return traps


def get_last_move(prev_board, board, last_player):
    if prev_board is None:
        return None
    start_pos, end_pos = None, None
    # print("----"*20)
    # print_board(prev_board)
    # print("----"*20)
    # print_board(board)
    # print(last_player)
    h, w = len(board), len(board[0])
    # print(h, w)
    for i in range(h):
        for j in range(w):
            if prev_board[i][j] == board[i][j]:
                continue
            if (prev_board[i][j] == 0 and board[i][j] == last_player):
                # print("end pos: ", (i,j))
                end_pos = (i,j)
            elif (prev_board[i][j] == last_player and board[i][j] == 0):
                start_pos = (i,j)
                # print("start pos: ", (i,j))
    if start_pos is None or end_pos is None:
        raise Exception("Last move is invalid move")
    return {
        'pos': start_pos,
        'move': Action((end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
    }