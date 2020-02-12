from enum import IntEnum

class ActionType(IntEnum):
    CHECK = 1
    CALL = 2
    RAISE = 3
    FOLD = 4
    ALL_IN = 5

