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

    def __str__(self) -> str:
        if self == Action.MOVE_UP:
            return "↑"
        elif self == Action.MOVE_DOWN:
            return "↓"
        elif self == Action.MOVE_LEFT:
            return "←"
        elif self == Action.MOVE_RIGHT:
            return "→"
        elif self == Action.MOVE_UP_LEFT:
            return "↖"
        elif self == Action.MOVE_DOWN_RIGHT:
            return "↘"
        elif self == Action.MOVE_UP_RIGHT:
            return "↗"
        elif self == Action.MOVE_DOWN_LEFT:
            return "↙"

    def get_opposite(self):
        return Action(-self.value)

    @staticmethod
    def get_positive_action():
        return [Action(-action.value) for action in list(Action)]






