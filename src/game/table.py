from typing import List

from src.common.models.game import PlayerID
from src.players.player import Player

"""
Convenience class to keep track of the people in a hand
"""
class Table:
    all_players_in_round = None
    players_active_in_round = None  # all_players - players all in
    all_players = None
    id_to_player = {}

    def __init__(self, players: List[Player]):
        self.all_players = players
        self.id_to_player = {}
        for player in players:
            self.id_to_player[player.id] = player

    def reset(self):
        self.all_players_in_round = self.all_players.copy()
        self.players_active_in_round = self.all_players.copy()

    def get_player(self, pid: PlayerID):
        if pid in self.id_to_player:
            return self.id_to_player[pid]
        assert False

    def remove_player_from_round(self, pid: PlayerID):
        self.remove_player_from_active(pid)
        self.all_players_in_round = self.players_active_in_round.copy()

    def remove_player_from_active(self, pid: PlayerID):
        ind = self.get_player_ind(pid)
        del self.players_active_in_round[ind]

    def get_num_players_active_in_round(self):
        return len(self.players_active_in_round)

    # Only works for players active in round
    def get_player_ind(self, pid: PlayerID):
        for i in range(len(self.players_active_in_round)):
            if self.players_active_in_round[i].id == pid:
                return i
        return -1

    # get players n spots to the left of players with ID pid
    def get_left_of_player(self, n: int, pid: PlayerID):
        ind = self.get_player_ind(pid)
        ind += n
        return self.players_active_in_round[ind % len(self.players_active_in_round)]
