from enum import IntEnum

"""
Note we set enum values to how many cards are shown
"""
class Street(IntEnum):
    PREFLOP = 0
    FLOP = 3
    TURN = 4
    RIVER = 5
