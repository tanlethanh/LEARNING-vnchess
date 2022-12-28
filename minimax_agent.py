import time

from minimax import Node, minimax

MIN = -1000
MAX = 1000


def move_same_time_slot():
    pass


def move_first_long():
    pass


def move_last_long():
    pass


def move_all(_prev_board, _board, _player, _remain_time_x, _remain_time_o):
    start = time.time()

    cur_node = Node(_prev_board, _board, _player)

    is_max = False if _player == -1 else True
    max_value, count_node = minimax(node=cur_node, is_max_player=is_max, alpha=MIN, beta=MAX, depth=0,
                                    max_depth=5)

    end = time.time()

    # print(f"Number of node: {count_node}")
    # print(f"Time to solve {end - start}")
    print(f"AVG per node: {(end - start) / count_node}")

    for child in cur_node.children:
        if max_value == child.get_value():
            start, end = child.action
            # print(f"\t MINIMAX move: {start} -> {end}")
            return child.action

    return None
