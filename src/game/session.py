from typing import Dict

from src.common.models.data import RoundRecord
from src.players.player import Player
from src.common.models.game import RoundInfo, Action, PlayerID, StreetInfo
from src.common.enums.action_type import ActionType as A
from src.common.enums.street import Street as G
from src.game.dealer import Dealer
from src.common.game_utils.ranker import *
from src.game.table import Table

"""
Represents one session of poker
"""
class Session:

    players = None
    big_blind = -1
    small_blind = -1
    buy_in = -1
    round_info = None
    dealer: Player = None

    deck_dealer = None
    table = None

    """
    :type players: players[]
    """
    def __init__(self, players, big_blind, buy_in, small_blind: int =-1):
        self.players = players
        self.big_blind = big_blind
        self.small_blind = big_blind//2
        if small_blind != -1:
            self.small_blind = small_blind
        self.buy_in = buy_in
        self.deck_dealer = Dealer()
        self.dealer = players[0]
        self.table = Table(players)

    # run one street of poker
    def run_street(self, r: RoundInfo, t: Table):
        street = r.current_street
        street_info = StreetInfo(r.all_community_cards[:street.value], t.players_active_in_round)
        r.street_info[street] = street_info

        # end if not enough players are in the round
        if t.get_num_players_active_in_round() <= 1:
            return False
        
        start_player: Player  # players who starts - this can change to whoever makes a raise
        if street == G.PREFLOP:
            start_player = t.get_left_of_player(3, r.dealer.id)
            # blinds
            BB = t.get_left_of_player(2, r.dealer.id)
            SB = t.get_left_of_player(1, r.dealer.id)
            BB.bet(self.big_blind)
            street_info.bets_by_player[BB.id] = self.big_blind
            SB.bet(self.small_blind)
            street_info.bets_by_player[SB.id] = self.small_blind
            street_info.pot += self.big_blind*1.5
            street_info.max_bet = self.big_blind
        else:
            start_player = t.get_left_of_player(1, r.dealer.id)
            r.max_bet = 0

        # play round
        current_player: Player = start_player
        while True:
            if t.get_num_players_active_in_round() <= 1:
                break
            act = current_player.respond(r)
            next_player = t.get_left_of_player(1, current_player.id)

            # record action
            street_info.actions.append(act)
            street_info.actions_by_player[act.player_id].append(act)
            # process action
            if act.action == A.FOLD:
                t.remove_player_from_round(current_player.id)
            elif act.action != A.CHECK:
                prev_bet = street_info.bets_by_player[current_player.id]
                current_player.unbet(prev_bet)
                current_player.bet(act.bet)
                street_info.pot -= prev_bet
                street_info.pot += act.bet
                street_info.bets_by_player[current_player.id] = act.bet
                if act.action == A.RAISE:
                    start_player = current_player
                    r.max_bet = act.bet
                elif act.action == A.ALL_IN:
                    t.remove_player_from_active(current_player.id)

            current_player = next_player
            if current_player == start_player:
                break
        return t.get_num_players_active_in_round() == 1

    def new_round(self, dealer: Player, cards: List[Card]):
        return RoundInfo(dealer, cards, self.big_blind//2, self.big_blind)

    """
    :return map of each player's id to their winnings
    """
    def get_players_winnings(self) -> Dict[PlayerID, int]:
        r = self.round_info
        latest_street = r.current_street
        latest_street_info = r.street_info[latest_street]
        # get a score for each hand
        scores = []
        for player in self.table.all_players_in_round:
            score = get_score(latest_street_info.community_cards + list(player.cards))
            scores.append((player, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        # for s in scores:
        #     print("Player %d hand: %s scored: %d" % (s[0].id, s[0].cards, s[1]))

        # distribute money
        # first, split players into groups of people who split the pot
        if len(scores) == 0:
            return {}
        groups: List[List[PlayerID]] = []
        currGroup = [scores[0][0].id]
        for i in range(1, len(scores)):
            if scores[i][1] < scores[i-1][1]:
                groups.append(currGroup)
                currGroup = [scores[i][0].id]
            else:
                currGroup.append(scores[i][0].id)
        groups.append(currGroup)
        # print("Groups: %s" % groups)
        # for each group, split pot appropriately
        players_to_winnings: Dict[PlayerID, int] = {}
        for player in self.table.all_players_in_round:
            players_to_winnings[player.id] = 0
        player_bets_by_street = []
        for street in r.street_info:
            player_bets_by_street.append(r.street_info[street].bets_by_player.copy())

        for group in groups:
            # go through player bets from every street from the end of array
            for i in range(len(player_bets_by_street)-1, -1, -1):
                player_bets = player_bets_by_street[i]
                # this group is everyone involved in the pot at the current street
                group_to_process = [i for i in filter(lambda x: x in player_bets, group)]
                group_to_process.sort(key=lambda x: player_bets[x])
                # go through people in current winning group
                for j in range(len(group_to_process)):
                    if group_to_process[j] not in player_bets or player_bets[group_to_process[j]] == 0:
                        continue
                    # calculate pot from person who bet the least
                    curr_pot = 0
                    bet_per_person_to_distribute = player_bets[group_to_process[j]]
                    for player_who_was_in in player_bets:
                        if player_bets[player_who_was_in] >= bet_per_person_to_distribute:
                            curr_pot += bet_per_person_to_distribute
                            player_bets[player_who_was_in] -= bet_per_person_to_distribute
                        else:
                            curr_pot += player_bets[player_who_was_in]
                            player_bets[player_who_was_in] = 0
                    # divide pot amongst all who won
                    for k in range(j, len(group_to_process)):
                        players_to_winnings[group_to_process[k]] += curr_pot//(len(group_to_process)-j)

                    # delete people with 0 bet in player_bets
                    to_delete = [key for key in player_bets if player_bets[key] == 0]
                    for k_to_del in to_delete:
                        del player_bets[k_to_del]
                if len(player_bets) == 0:
                    del player_bets_by_street[i]
        return players_to_winnings

    """
    run one round of poker from start to finish
    :return Round Record
    """
    def run_round(self) -> RoundRecord:
        # Deal cards
        community_cards = self.deck_dealer.deal(self.players)
        # print("Community cards: %s" % community_cards)
        player_hands = {}
        for player in self.players:
            player_hands[player.id] = player.cards

        # Initialize round
        self.table.reset()
        self.round_info = self.new_round(self.dealer, community_cards)
        
        # Run rounds
        game_finished = self.run_street(self.round_info, self.table)
        if not game_finished:
            self.round_info.current_street = G.FLOP
            game_finished = self.run_street(self.round_info, self.table)
        if not game_finished:
            self.round_info.current_street = G.TURN
            game_finished = self.run_street(self.round_info, self.table)
        if not game_finished:
            self.round_info.current_street = G.RIVER
            self.run_street(self.round_info, self.table)

        # distribute winnings
        players_to_winnings: Dict[PlayerID, int] = self.get_players_winnings()
        # print(players_to_winnings)
        for player in self.players:
            if player.id in players_to_winnings:
                player.win_money(players_to_winnings[player.id])
        round_record = RoundRecord(self.round_info, player_hands, players_to_winnings)

        # shift dealer
        self.table.reset()
        self.dealer = self.table.get_left_of_player(1, self.dealer.id)

        return round_record

    """
    Modifier Functions
    """

    def set_dealer(self, dealer_id: PlayerID):
        self.dealer = self.table.get_player(dealer_id)

    def set_deck_biases(self, new_deck_biases):
        self.deck_dealer.set_deck_biases(new_deck_biases)

    def set_com_cards(self, new_com_cards):
        self.deck_dealer.set_com_cards(new_com_cards)

    def clear_deck_biases(self):
        self.deck_dealer.clear_deck_biases()

    def clear_com_cards(self):
        self.deck_dealer.clear_com_cards()
