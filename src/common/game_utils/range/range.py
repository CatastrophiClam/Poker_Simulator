import os
from typing import List, Tuple

from src.common.enums.card import Card
from src.common.game_utils.range.range_preset import RangePreset, RANGE_PRESET_TO_FILE


def get_grid_from_file(file_path: str) -> List[List[float]]:
    file = None
    try:
        file = open(file_path, "r")
        lines = file.readlines()
        grid = []
        for line in lines:
            probs = line.strip().split(" ")
            grid.append([float(i) for i in probs])
    except():
        if file is not None and not file.closed:
            file.close()
        raise
    return grid

"""
range object:
    A K Q 10 J 9 8 7 6 5 4 3 2
A   O O O O  O O O O O O O O O
K   S O O O  O
Q   S S O O  O
J   S S S O  O
10  x x x x  x
9  ...
8
7
6
5
4
3
2

suited is row > col, unsuited is row <= col
each cell is the probability of play the hand if that hand is dealt
"""

# Redo
class Range:
    grid: List[List[float]]

    def __init__(self, grid=None, preset: RangePreset = None):
        if grid is not None:
            self.grid = grid
        if preset is not None:
            self.grid = get_grid_from_file(RANGE_PRESET_TO_FILE[preset])
        if len(self.grid) != 13:
            raise Exception("Error: invalid grid - grid does not have 13 rows")
        for i in range(len(self.grid)):
            if len(self.grid[i]) != 13:
                raise Exception("Error: invalid grid - grid[{0}] does not have 13 columns".format(i))

    def __str__(self):
        card_labels = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        label_string = [i.ljust(7) for i in card_labels]
        answer = "   "+"".join(label_string)+"\n"
        for i in range(len(self.grid)):
            s = card_labels[i].ljust(3) + " ".join(["{:.4f}".format(f).ljust(6) for f in self.grid[i]]) + "\n"
            answer += s
        return answer

    """
    :return tuple(r, c) for grid of cards - returns suited cell if cards are suited, unsuited if not
    """
    @staticmethod
    def get_r_c(c1: Card, c2: Card) -> Tuple[int, int]:
        c1_ind: int = 13 - c1.value
        c2_ind: int = 13 - c2.value
        if c1 // 13 == c2 // 13:
            return min(c1_ind, c2_ind), max(c1_ind, c2_ind)
        else:
            return max(c1_ind, c2_ind), min(c1_ind, c2_ind)

    # Note, passing any 2 unsuited cards will set the unsuited cell, passing 2 suited will set the suited cell
    def set_cell_probability(self, c1: Card, c2: Card, new_probability):
        loc = self.get_r_c(c1, c2)
        self.grid[loc[0]][loc[1]] = new_probability

    def __repr__(self):
        return self.__str__()

    def save_to_file(self, file_name):
        file = open(os.getcwd() + "/common/game_utils/range/saved_ranges/" + file_name, "w")
        lines = [" ".join([str(i) for i in j])+"\n" for j in self.grid]
        file.writelines(lines)
        file.close()

    def is_in_self(self, cards: Tuple[Card, Card]):
        a = max(cards[0].value % 13, cards[1].value % 13)
        b = min(cards[0].value % 13, cards[1].value % 13)
        if cards[0].value // 13 == cards[1].value // 13:
            return self.grid[a][b] > 0
        else:
            return self.grid[b][a] > 0

    def clone(self):
        return Range([i.copy for i in self.grid])
