from enum import Enum
class Action(Enum):
    MOVE_UP = 1
    MOVE_DOWN = -1
    MOVE_LEFT = 2
    MOVE_RIGHT = -2
    MOVE_UP_LEFT = 3
    MOVE_DOWN_RIGHT = -3
    MOVE_UP_RIGHT = 4
    MOVE_DOWN_LEFT = -4


class Chess :

    def __init__(board):
        pass


    def move_chess_man(start: tuple(int, int), action: Action)-> tuple(int,int):
        # TODO:
        pass

    def get_valid_actions(index: tuple(int, int)) -> list[Action]:
        # TODO:
        pass

    def update_board(board: list[list[int]], start: tuple(int, int), action: Action) -> list[list[int]]:
    # TODO
        pass
    
def move(board: list[list[int]], index : tuple(int, int), action: Action) ->tuple(tuple(int,int),tuple(int,int)): 
    # TODO:
    pass

def get_traps(prev_board: list[list[int]], curr_board: list[list[int]]) -> list[tuple(tuple(int, int), Action)]:
    # TODO: Exact trap from lastest move of opponent
    pass

