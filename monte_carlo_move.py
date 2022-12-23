from monte_agent import *
from monte_chess_state import *
from monte_carlo_tree_search import *
from monte_nodes import *
from monte_utils import *

def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    if _player == 1:
        _remain_time = _remain_time_x
    else:
        _remain_time = _remain_time_o
    monte = MonteAgent(_prev_board, _board,_player,remain_duration=_remain_time,level='expert')
    best_move = monte.move().parent_action
    start = best_move['pos']
    end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
    return (start, end)