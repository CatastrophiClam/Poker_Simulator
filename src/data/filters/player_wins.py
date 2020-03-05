from src.common.models.data import RoundRecord
from src.common.models.game import PlayerID
from src.data.base_filter import BaseFilter


class PlayerWins(BaseFilter):

    def __init__(self, pid: PlayerID):
        self.pid = pid

    def check(self, record: RoundRecord):
        return record.winners_to_winnings[self.pid] > 0

    def __str__(self):
        return "Player {0} wins".format(self.pid)
