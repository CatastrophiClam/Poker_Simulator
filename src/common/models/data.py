from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from src.common.models.game import PlayerID, Action, StreetInfo, RoundInfo
from src.common.enums.card import Card
from src.common.enums.street import Street

@dataclass
class StreetRecord:
    actions: List[Action]
    actions_by_player: Dict[PlayerID, List[Action]]
    bets_by_player: Dict[PlayerID, int]
    players_involved: Set[PlayerID]
    final_pot: int

    def __init__(self, street_info: StreetInfo):
        self.actions = street_info.actions.copy()
        self.actions_by_player = street_info.actions_by_player.copy()
        self.bets_by_player = street_info.bets_by_player.copy()
        self.players_involved = set()
        for player in street_info.actions_by_player:
            self.players_involved.add(player)
        self.final_pot = street_info.pot

@dataclass(frozen=True)
class RoundRecord:
    street_record: Dict[Street, StreetRecord]
    dealer: int
    community_cards: List[Card]
    small_blind: int
    big_blind: int
    player_cards: Dict[PlayerID, Tuple[Card, Card]]
    winners_to_winnings: Dict[PlayerID, int]
    net_winnings_by_player: Dict[PlayerID, int]
    players_to_hand_score: Dict[PlayerID, int]

    def __init__(self, round_info: RoundInfo, player_cards: Dict[PlayerID, Tuple[Card, Card]], winners_to_winnings: Dict[PlayerID, int]):
        object.__setattr__(self, "street_record", {})
        for street in round_info.street_info:
            self.street_record[street] = StreetRecord(round_info.street_info[street])
        object.__setattr__(self, "dealer", round_info.dealer)
        object.__setattr__(self, "community_cards", round_info.all_community_cards)
        object.__setattr__(self, "small_blind", round_info.small_blind)
        object.__setattr__(self, "big_blind", round_info.big_blind)
        object.__setattr__(self, "players_to_hand_score", round_info.players_to_hand_score)
        object.__setattr__(self, "player_cards", player_cards.copy())
        object.__setattr__(self, "winners_to_winnings", winners_to_winnings.copy())
        temp_net_winnings_by_player = {}
        for street in round_info.street_info:
            for pid in round_info.street_info[street].bets_by_player:
                if pid not in temp_net_winnings_by_player:
                    temp_net_winnings_by_player[pid] = 0
                temp_net_winnings_by_player[pid] -= round_info.street_info[street].bets_by_player[pid]
        for pid in self.winners_to_winnings:
            temp_net_winnings_by_player[pid] += self.winners_to_winnings[pid]
        object.__setattr__(self, "net_winnings_by_player", temp_net_winnings_by_player)

@dataclass(frozen=True)
class Category:
    category: int
    description: str

    def __eq__(self, other):
        return self.category == other.category and self.description == other.description

    def __hash__(self):
        return hash((self.category, self.description))
