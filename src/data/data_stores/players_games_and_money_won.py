from typing import Dict

from src.common.models.data import RoundRecord
from src.common.models.game import PlayerID
from src.data.base_data_store import BaseDataStore


class PlayersGamesAndMoneyWon(BaseDataStore):
    games_won_no_tie_by_player: Dict[PlayerID, int]
    games_won_with_tie_by_player: Dict[PlayerID, int]
    winnings_by_player:Dict[PlayerID, int]
    total_games_recorded: int
    big_blind: int

    def __init__(self):
        self.total_games_recorded = 0
        self.games_won_no_tie_by_player = {}
        self.games_won_with_tie_by_player = {}
        self.winnings_by_player = {}

    def handle_console_queries(self):
        pids = [i for i in self.games_won_no_tie_by_player]
        for pid in self.games_won_with_tie_by_player:
            if pid not in pids:
                pids.append(pid)
        pids.sort()
        for pid in pids:
            big_blinds_per_game = self.winnings_by_player[pid] / self.total_games_recorded / self.big_blind
            games_won = self.games_won_no_tie_by_player[pid] if pid in self.games_won_no_tie_by_player else 0
            games_won_with_tie = self.games_won_with_tie_by_player[pid] if pid in self.games_won_with_tie_by_player else 0
            print("Player %d (net %d chips, %f BBs per game): won %d without ties, won %d with ties out of %d games" %
                  (pid, self.winnings_by_player[pid], big_blinds_per_game, games_won,
                   games_won_with_tie, self.total_games_recorded))
        print()

    def record(self, round_record: RoundRecord) -> bool:
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
                if pid not in self.games_won_with_tie_by_player:
                    self.games_won_with_tie_by_player[pid] = 0
                self.games_won_with_tie_by_player[pid] += 1
            else:
                if pid not in self.games_won_no_tie_by_player:
                    self.games_won_no_tie_by_player[pid] = 0
                self.games_won_no_tie_by_player[pid] += 1

        # Record money won
        for pid in round_record.net_winnings_by_player:
            if pid not in self.winnings_by_player:
                self.winnings_by_player[pid] = 0
            self.winnings_by_player[pid] += round_record.net_winnings_by_player[pid]
        self.total_games_recorded += 1
        return True

    def __str__(self):
        return "Number of games won by players, differentiated by ties allowed or not allowed"

    def __repr__(self):
        return self.__str__()
