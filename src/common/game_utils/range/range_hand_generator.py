import random
from typing import Tuple, List

from src.common.enums.card import Card
from src.common.game_utils.range.range import Range


class RangeHandGenerator:

    def __init__(self, hand_range: Range):
        self.possible_hands = []
        self.probabilities = []
        self.cum_probabilities = []
        grid = hand_range.grid
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] > 0:
                    # append card values and whether they're suited
                    self.possible_hands.append((12-r, 12-c, c > r))
                    self.probabilities.append(grid[r][c])

        total = 0
        for p in self.probabilities:
            total += p
            self.cum_probabilities.append(total)

    """
    Generate a hand relative probabilities - for example if AA had 100% and KK had 50% 
    this would generate AA 66% of the time and KK 33 % of the time
    """
    def generate_weighted(self) -> Tuple[Card, Card]:
        raw_hand = random.choices(self.possible_hands, cum_weights=self.cum_probabilities)[0]
        c1, c2, is_suited = raw_hand
        if c1 == c2:
            hand = random.sample([c1, c1+13, c1+26, c1+39], 2)
            return Card(hand[0]), Card(hand[1])
        else:
            if is_suited:
                suit = random.sample([0, 1, 2, 3], 1)
                return Card(c1+13*suit), Card(c2+13*suit)
            else:
                return Card(random.choices([c1, c1+13, c1+26, c1+39], k=1)[0]), \
                       Card(random.choices([c2, c2+13, c2+26, c2+39], k=1)[0])

    """
    Generate hand with each hand in range having equal probability
    """
    def generate_unweighted(self) -> Tuple[Card, Card]:
        raw_hand = random.choices(self.possible_hands)[0]
        c1, c2, is_suited = raw_hand
        if c1 == c2:
            hand = random.choices([c1, c1 + 13, c1 + 26, c1 + 39], k=2)
            return Card(hand[0]), Card(hand[1])
        else:
            if is_suited:
                suit = random.choices([0, 1, 2, 3])
                return Card(c1 + 13 * suit), Card(c2 + 13 * suit)
            else:
                return Card(random.choices([c1, c1 + 13, c1 + 26, c1 + 39], k=1)[0]), \
                       Card(random.choices([c2, c2 + 13, c2 + 26, c2 + 39], k=1)[0])