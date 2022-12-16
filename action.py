from enum import Enum


class Action(Enum):
    MOVE_UP = (1, 0)
    MOVE_DOWN = (-1, 0)
    MOVE_LEFT = (0, -1)
    MOVE_RIGHT = (0, 1)
    MOVE_UP_LEFT = (1, -1)
    MOVE_DOWN_RIGHT = (-1, 1)
    MOVE_UP_RIGHT = (1, 1)
    MOVE_DOWN_LEFT = (-1, -1)

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
        x, y = self.value
        return Action((-x, -y))

    @staticmethod
    def get_half_actions():
        return [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_UP_RIGHT, Action.MOVE_UP_LEFT]
