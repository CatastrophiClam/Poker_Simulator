from enum import IntEnum
import os

"""
Note we set enum values to how many cards are shown
"""
class RangePreset(IntEnum):
    ALL = 0
    GENERIC_PREFLOP = 1

PATH_TO_PRESET_FILES = os.getcwd() + "/common/game_utils/range/range_preset_files/"

RANGE_PRESET_TO_FILE = {
    RangePreset.ALL: PATH_TO_PRESET_FILES + "all_cards_range.txt",
    RangePreset.GENERIC_PREFLOP: PATH_TO_PRESET_FILES + "generic_preflop_range.txt"
}
