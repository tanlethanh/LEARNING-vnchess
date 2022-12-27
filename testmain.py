# model test đánh với người thường
# Nếu một moveTupple không hợp lệ thì bắt chọn lại moveTupple

# Import thư viện và hàm
import random
import time
import minimax

def main():
    # Khởi tạo bàn cờ đầu tiên
    start_board = [[1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 0, 0, 0, -1],
                    [-1, 0, 0, 0, -1],
                    [-1, -1, -1, -1, -1]]
    master_board = State(None, start_board)
    # Chọn ai đi trước và ai là 'X' (-1) hoặc 'O' (1)
    side = int(input("Input your side, 1 or -1: "))
    # Yêu cầu nhập xem ai là 'X' hoặc 'O'
    turn = int(input("Who go first (1_(O) | -1_(X)) ?"))
    # Set thời gian cho người chơi
    remain_time = {
        "remain_time_x": 20000,
        "remain_time_o": 20000
    }

    while True:
        # User Turn
        if turn == side:
            isPossibleMove = False
            #Start user time
            s_user_time = time.time()
            while not isPossibleMove:
                print("Please input a valid move.")
                printCanPickPiece(master_board, turn)
                startString = input("Input position of picked piece: ")
                startTuple = eval(startString)
                if printCanPickDes(master_board, startTuple) == False: continue
                endString = input("Input position of destination: ")
                #End user Time
                e_user_time = time.time()
                endTuple = eval(endString)
                moveTuple = (startTuple, endTuple)
                if master_board.boardMoveChk(moveTuple, side) == False: continue 
                else: isPossibleMove = True
            # Giảm thời gian chơi của user
            if side == 1:
                remain_time["remain_time_x"] -= s_user_time - e_user_time
            else:
                remain_time["remain_time_o"] -= s_user_time - e_user_time

        # Com turn
        else:
            # # Random piece in pieceList
            # piece = random.choice(master_board.pieceList)
            # # Random move in pieceList.possibleMove
            # moveTuple = random.choice(piece.posibleMove)
            s_com_time = time.time()
            moveTuple = move(master_board.prev_board, master_board.board, side*(-1), remain_time["remain_time_x"], remain_time["remain_time_o"])
            e_com_time = time.time()
            print("Computer decision time: ", e_com_time - s_com_time)
            print("Computer make move: ", moveTuple)
        master_board.boardMove(moveTuple)

        # Kiểm tra thời gian còn lại của X và O
        if remain_time["remain_time_x"] <= 0:
            print("End of game, player X is out of time!")
        elif remain_time["remain_time_o"] <= 0:
            print("End of game, player Y is out of time!")

        # Viết file txt kết quả:
        nowBoard = master_board.board
        writeStateFile("test/pve.txt", nowBoard)

        # In kết quả ra terminal:
        printState(nowBoard)

        # Kiểm tra thắng cuộc
        if master_board.victor:
            print("End of game, the victory is " + str(side))
            break
        turn *= -1
    return


if __name__ == "__main__":
    main()