import time
from abc import ABC
from typing import List

from src.console.data_console import DataConsole
from src.data.base_data_store import BaseDataStore
from src.data.data_tracker import DataTracker
from src.players.player import Player


class BaseExperiment(ABC):

    def __init__(self):
        self.num_hands_per_session: int = 0
        self.starting_money: int = 0
        self.big_blind: int = 0
        self.persistent_log_threshold: int = 0
        self.players: List[Player] = []
        self.data_stores: List[BaseDataStore] = []
        self.session = None

    def run(self):
        data_tracker = DataTracker(self.persistent_log_threshold, self.data_stores)

        # run game num_hands_per_session times
        start_time = time.process_time_ns()
        for i in range(self.num_hands_per_session):
            info = self.session.run_round()
            for player in self.players:
                if player.money < self.starting_money / 2:
                    player.rebuy()
            data_tracker.log(info)
            if i != 0 and i % 50000 == 0:
                print("Processed %d hands" % i)
        end_time = time.process_time_ns()

        print("Processed %d hands in %f seconds" % (self.num_hands_per_session, (end_time - start_time) // 1000000 / 1000))
        print()

        # Start data console
        data_console = DataConsole(self.data_stores)
        data_console.start_data_console()
