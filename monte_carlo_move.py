
def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    if _player == 1:
        _remain_time = _remain_time_x
    else:
        _remain_time = _remain_time_o
    monte = MonteAgent(_prev_board, _board,_player,remain_duration=_remain_time,level='expert')
    best_child = monte.move()
    best_move = best_child.parent_action
    start = best_move['pos']
    end = (start[0] + best_move['move'].value[0], start[1] + best_move['move'].value[1])
    assert(isinstance(best_child, ChessVNNode))
    print(f"\t MONTE move: {start} -> {end}")
    return (start, end)