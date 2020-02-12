from dataclasses import dataclass
from typing import List, Dict, Tuple, TYPE_CHECKING

from src.common.enums.action_type import ActionType
from src.common.enums.card import Card
from src.common.enums.street import Street
if TYPE_CHECKING:
    from src.players.player import Player

PlayerID = int

@dataclass(frozen=True)
class Action:
    action: ActionType
    # Note that this is a bet TO a value
    # For example, if players A bets, B raises him, then A re raises
    # bet will be the total amount A has bet this street, not the difference between A's bet and re raise
    bet: int = -1
    player_id: PlayerID = -1
    reason: int = -1

@dataclass
class StreetInfo:
    community_cards: List[Card]
    actions: List[Action]
    actions_by_player: Dict[PlayerID, List[Action]]
    bets_by_player: Dict[PlayerID, int]
    pot: int      # will change as the street progresses, should end at final value at end of street
    max_bet: int  # will change as the street progresses, should end at final value at end of street

    def __init__(self, community_cards: List[Card], players: List['Player']):
        self.community_cards = community_cards
        self.actions = []
        self.actions_by_player = {}
        self.bets_by_player = {}
        self.pot = 0
        self.max_bet = 0
        for player in players:
            self.actions_by_player[player.id] = []
            self.bets_by_player[player.id] = 0

@dataclass
class RoundInfo:
    current_street: Street
    dealer: 'Player'
    all_community_cards: List[Card]
    small_blind: int
    big_blind: int
    street_info: Dict[Street, StreetInfo]

    def __init__(self, dealer: 'Player', all_community_cards: List[Card], small_blind: int, big_blind: int):
        self.current_street = Street.PREFLOP
        self.dealer = dealer
        self.all_community_cards = all_community_cards
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.street_info = {}

@dataclass
class OrganizedHand:
    cards: List[Card]  # sorted ascending
    hand: List[Card]  # 5 max, sorted ascending
    pairs: List[int]  # of the paired cards
    trips: List[int]  # of the trip cards
    quads: List[int]  # of the quad card
    has_flush: bool = False
    has_straight: bool = False
    has_straight_flush: bool = False
