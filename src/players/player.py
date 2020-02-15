from typing import Tuple

from src.common.models.game import PlayerID, RoundInfo
from src.common.enums.card import Card
from src.players.base_player_profile import BasePlayerProfile


"""
Keeps track of the money and cards and enacts actions of a player throughout a session
"""
class Player:
    player_profile: BasePlayerProfile
    money: int
    starting_money: int
    id: PlayerID
    cards = Tuple[Card, Card]
    current_bet: int
    total_money_invested: int

    def __init__(self, player_profile: BasePlayerProfile, starting_money: int, pid: PlayerID):
        self.player_profile = player_profile
        self.money = starting_money
        self.id = pid
        self.starting_money = starting_money
        self.total_money_invested = starting_money
        self.player_profile.id = pid
        self.wins = 0

    def deal(self, cards: Tuple[Card, Card]):
        self.cards = cards

    def bet(self, amount: int):
        self.money -= amount

    def unbet(self, amount: int):
        self.money += amount

    def rebuy(self):
        self.total_money_invested += self.starting_money - self.money
        self.money = self.starting_money

    def win_money(self, amount: int):
        self.money += amount

    def respond(self, info: RoundInfo):
        ans = self.player_profile.respond(info, self.cards)
        return ans