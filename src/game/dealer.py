from typing import Dict, List, Tuple

from src.common.models.game import PlayerID
from src.common.enums.card import Card as C
import random

from src.common.enums.card import Card
from src.players.player import Player


class Dealer:

    # Allows us to give certain players certain cards
    # Note we can set only one card for a players by setting the other card in the tuple to None
    deck_biases: Dict[PlayerID, Tuple[Card, Card]] = {}

    # Allows us to set community cards
    # Ordered from flop to turn
    # Eg. [null, null, null, S2, C4] sets no cards for the flop, S2 for turn and C4 for river
    com_cards: List[Card] = []

    """
    :param players: Note we don't modify players list
    :return list of community cards
    """
    def deal(self, players: List[Player]) -> List[Card]:
        available_cards: List[Card] = [i for i in C if i not in self.com_cards]

        # first deal players with set cards
        for player in players:
            player_hand: List[Card] = []
            if player.id in self.deck_biases:
                if type(self.deck_biases[player.id]) == tuple:
                    hand_to_set = self.deck_biases[player.id]
                    if hand_to_set[0] is not None:
                        player_hand.append(hand_to_set[0])
                        available_cards.remove(hand_to_set[0])
                    if hand_to_set[1] is not None:
                        player_hand.append(hand_to_set[1])
                        available_cards.remove(hand_to_set[1])
                else:
                    # TODO: generate a hand from range
                    print("Hand generation from range isn't implemented yet")
            while len(player_hand) < 2:
                ind = random.randint(0, len(available_cards) - 1)
                player_hand.append(available_cards[ind])
                del available_cards[ind]
            player.deal((player_hand[0], player_hand[1]))

        # generate community cards
        returned_com_cards = []
        for i in range(5):
            card = None
            if i < len(self.com_cards):
                card = self.com_cards[i]
            if card is None:
                ind = random.randint(0, len(available_cards) - 1)
                card = available_cards[ind]
                del available_cards[ind]
            returned_com_cards.append(card)

        return returned_com_cards

    def set_com_cards(self, new_com_cards: List[Card]):
        self.com_cards = new_com_cards

    def set_deck_biases(self, new_deck_biases: Dict[PlayerID, Tuple[Card, Card]]):
        self.deck_biases = new_deck_biases

    def clear_com_cards(self):
        self.com_cards = []

    def clear_deck_biases(self):
        self.deck_biases = {}
