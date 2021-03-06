from typing import List

from src.data.base_data_store import BaseDataStore
from src.data.data_stores.players_games_and_money_won import PlayersGamesAndMoneyWon
from src.experiments.base_experiment import BaseExperiment
from src.game.session import Session
from src.players.player import Player
from src.players.ai.profiles.v0.profile import PlayerProfile as ProfileV0


class E0_0_0(BaseExperiment):

    def __init__(self):
        self.num_hands_per_session: int = 10000
        self.starting_money: int = 100000
        self.big_blind: int = 500
        self.persistent_log_threshold: int = 50000
        player_profiles = [ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0()]
        self.players = [Player(player_profiles[i], self.starting_money, i) for i in range(len(player_profiles))]
        self.data_stores = [PlayersGamesAndMoneyWon()]
        self.session = Session(self.players, self.big_blind, self.starting_money)