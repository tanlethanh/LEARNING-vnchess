import re

def humanmove(prev_board, board , player,
                                _remain_time_x, _remain_time_o):
    move = input("Input move: ")
    move = ''.join(x for x in move if x.isdigit())
    print(move)
    x1 = int(move[0])
    x2 = int(move[1])
    start = (x1, x2)

    x3 = int(move[2])
    x4 = int(move[3])
    end = (x3, x4)
    return (start, end)

if __name__ == "__main__":
    start, end = humanmove()
    print(start, end)