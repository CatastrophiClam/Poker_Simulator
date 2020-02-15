import unittest

from src.common.models.game import RoundInfo, StreetInfo
from src.game.session import Session, get_players_winnings
from src.players.ai.profiles.v0.profile import PlayerProfile as ProfileV0
from src.common.enums.card import Card as C
from src.common.game_utils.ranker import *
from src.common.enums.street import Street as S
from src.players.player import Player


class TestSplitWinnings(unittest.TestCase):
    STARTING_MONEY = 100000
    BIG_BLIND = 500

    def setUp(self) -> None:
        player_profiles = [ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0()]
        self.players = [Player(player_profiles[i], self.STARTING_MONEY, i) for i in range(len(player_profiles))]
        self.session = Session(self.players, self.BIG_BLIND, self.STARTING_MONEY)
        self.session.round_info = RoundInfo(self.players[0], [], self.BIG_BLIND // 2, self.BIG_BLIND)
        self.session.table.reset()

    def test_win_with_folds(self):
        self.session.round_info.current_street = S.TURN
        self.session.round_info.all_community_cards = [C.C2, C.S4, C.D5, C.H6, C.C8]
        self.players[0].deal((C.CA, C.DA))
        self.players[1].deal((C.SA, C.HA))
        self.players[2].deal((C.CK, C.SK))
        self.players[3].deal((C.DK, C.HK))
        self.players[4].deal((C.CQ, C.SQ))
        self.players[5].deal((C.DQ, C.HQ))
        self.session.round_info.street_info[S.PREFLOP] = StreetInfo(
            self.session.round_info.all_community_cards[:0], self.players)
        self.session.round_info.street_info[S.FLOP] = StreetInfo(
            self.session.round_info.all_community_cards[:3], self.players)
        self.session.round_info.street_info[S.TURN] = StreetInfo(
            self.session.round_info.all_community_cards[:4], self.players)
        self.session.round_info.street_info[S.RIVER] = StreetInfo(
            self.session.round_info.all_community_cards[:5], self.players)
        self.session.round_info.street_info[S.PREFLOP].bets_by_player = {
            0: 500, 1: 500, 2: 500, 3: 500, 4: 500, 5: 500
        }
        self.session.round_info.street_info[S.FLOP].bets_by_player = {
            0: 500, 1: 200, 2: 500, 3: 500, 4: 500, 5: 500
        }
        self.session.round_info.street_info[S.TURN].bets_by_player = {
            0: 500, 1: 0, 2: 100, 3: 200, 4: 500, 5: 500
        }
        self.session.table.remove_player_from_round(1)
        self.session.table.remove_player_from_round(2)
        self.session.table.remove_player_from_round(3)
        self.session.table.remove_player_from_round(4)
        self.session.table.remove_player_from_round(5)
        winnings = get_players_winnings(self.session.round_info, self.session.table)
        self.assertEqual({0: 7500}, winnings)

    def test_3_tier_tie(self):
        self.session.round_info.current_street = S.RIVER
        self.session.round_info.all_community_cards = [C.C2, C.S4, C.D5, C.H6, C.C8]
        self.players[0].deal((C.CA, C.DA))
        self.players[1].deal((C.SA, C.HA))
        self.players[2].deal((C.CK, C.SK))
        self.players[3].deal((C.DK, C.HK))
        self.players[4].deal((C.CQ, C.SQ))
        self.players[5].deal((C.DQ, C.HQ))
        self.session.round_info.street_info[S.PREFLOP] = StreetInfo(
            self.session.round_info.all_community_cards[:0], self.players)
        self.session.round_info.street_info[S.FLOP] = StreetInfo(
            self.session.round_info.all_community_cards[:3], self.players)
        self.session.round_info.street_info[S.TURN] = StreetInfo(
            self.session.round_info.all_community_cards[:4], self.players)
        self.session.round_info.street_info[S.RIVER] = StreetInfo(
            self.session.round_info.all_community_cards[:5], self.players)
        self.session.round_info.street_info[S.PREFLOP].bets_by_player = {
            0: 500, 1: 500, 2: 500, 3: 500, 4: 500, 5: 500
        }
        self.session.round_info.street_info[S.FLOP].bets_by_player = {
            0: 100, 1: 200, 2: 500, 3: 500, 4: 500, 5: 500
        }
        self.session.round_info.street_info[S.TURN].bets_by_player = {
            0: 0, 1: 0, 2: 100, 3: 200, 4: 500, 5: 500
        }
        self.session.round_info.street_info[S.RIVER].bets_by_player = {
            0: 0, 1: 0, 2: 0, 3: 0, 4: 100, 5: 200
        }
        winnings = get_players_winnings(self.session.round_info, self.session.table)
        self.assertEqual({0: 1800, 1: 2300, 2: 800, 3: 1100, 4: 400, 5: 500}, winnings)

