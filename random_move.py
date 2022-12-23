import random

from minimax import get_all_actions


def move(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    actions = get_all_actions(_prev_board, _board, _player)
    index = random.randint(0, len(actions) - 1)
    start, end = actions[index]

    print(f"\t RANDOM move: {start} -> {end}")
    return start, end
