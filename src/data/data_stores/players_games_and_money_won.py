from typing import Dict, List

from src.common.models.data import RoundRecord
from src.common.models.game import PlayerID
from src.data.base_filter import BaseFilter
from src.data.non_accumulative_data_store import NonAccumulativeDataStore


class PlayersGamesAndMoneyWon(NonAccumulativeDataStore):

    big_blind: int

    def __init__(self, filters: List[BaseFilter]):
        super().__init__(filters)

    def initialize_segment(self, segment, is_segment_unfiltered_segment=False):
        segment['games_won_no_tie_by_player'] = {}
        segment['games_won_with_tie_by_player'] = {}
        segment['winnings_by_player'] = {}
        segment['games_recorded_in_segment'] = 0

    def print_data(self):
        segment = self.segment_to_display
        pids = [i for i in segment['games_won_no_tie_by_player']]
        for pid in segment['games_won_with_tie_by_player']:
            if pid not in pids:
                pids.append(pid)
        pids.sort()
        for pid in pids:
            big_blinds_per_game = segment['winnings_by_player'][pid] / segment['games_recorded_in_segment'] / self.big_blind
            games_won = segment['games_won_no_tie_by_player'][pid] \
                if pid in segment['games_won_no_tie_by_player'] else 0
            games_won_with_tie = segment['games_won_with_tie_by_player'][pid] \
                if pid in segment['games_won_with_tie_by_player'] else 0
            print("Player %d (net %d chips, %f BBs per game): won %d without ties, won %d with ties out of %d games" %
                  (pid, segment['winnings_by_player'][pid], big_blinds_per_game, games_won,
                   games_won_with_tie, segment['games_recorded_in_segment']))
        print()

    def record_segment(self, data_segment, is_segment_unfiltered_segment: bool, round_record: RoundRecord) -> bool:
        winners = set()
        max_score = -1
        self.big_blind = round_record.big_blind

        # Record games won
        for pid in round_record.players_to_hand_score:
            # We need to find the highest score out of the people that won money
            # Note if someone has a higher score but didn't win money that means they folded so we can't count that
            if round_record.players_to_hand_score[pid] > max_score and round_record.winners_to_winnings[pid] > 0:
                max_score = round_record.players_to_hand_score[pid]
        for pid in round_record.players_to_hand_score:
            if round_record.players_to_hand_score[pid] == max_score:
                winners.add(pid)
        for pid in winners:
            if len(winners) > 1:
                if pid not in data_segment['games_won_with_tie_by_player']:
                    data_segment['games_won_with_tie_by_player'][pid] = 0
                data_segment['games_won_with_tie_by_player'][pid] += 1
            else:
                if pid not in data_segment['games_won_no_tie_by_player']:
                    data_segment['games_won_no_tie_by_player'][pid] = 0
                data_segment['games_won_no_tie_by_player'][pid] += 1

        # Record money won
        for pid in round_record.net_winnings_by_player:
            if pid not in data_segment['winnings_by_player']:
                data_segment['winnings_by_player'][pid] = 0
            data_segment['winnings_by_player'][pid] += round_record.net_winnings_by_player[pid]
        data_segment['games_recorded_in_segment'] += 1
        return True

    def __str__(self):
        return "Number of games won by players, differentiated by ties allowed or not allowed"

    def __repr__(self):
        return self.__str__()
