from game_manager import get_traps, copy_board
from utils import print_board


def trap_points(traps):
    trap_points = []
    for trap in traps:
        if trap[1] not in trap_points:
            trap_points.append(trap[1])
    return trap_points


if __name__ == "__main__":

    # Two traps
    print("TWO TRAPS")
    board_1 = [[1, 1, 0, 1, 1],
               [1, 0, 1, 0, 1],
               [1, -1, -1, 0, -1],
               [-1, 0, 0, 0, -1],
               [-1, 0, 0, -1, -1]]

    traps = get_traps(board_1, (1, 2), -1)

    traps_point = trap_points(traps)

    new_board_1 = copy_board(board_1)
    for tp in traps_point:
        x, y = tp
        new_board_1[x][y] = '*'

    print_board(new_board_1)
    print(traps)

    # No traps
    print("NO TRAP")
    board_1 = [[1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1],
               [1, 0, 0, 0, -1],
               [-1, 0, 0, 0, -1],
               [-1, -1, -1, -1, -1]]

    traps = get_traps(board_1, (1, 2), -1)

    traps_point = trap_points(traps)

    new_board_1 = copy_board(board_1)
    for tp in traps_point:
        x, y = tp
        new_board_1[x][y] = '*'

    print_board(new_board_1)
    print(traps)
