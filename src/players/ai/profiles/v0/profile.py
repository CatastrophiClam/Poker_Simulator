from typing import List

from src.common.models.data import RoundRecord
from src.common.models.game import RoundInfo, Action
from src.common.enums.action_type import ActionType as A
from src.common.enums.card import Card
from src.players.base_player_profile import BasePlayerProfile


class PlayerProfile(BasePlayerProfile):

    def respond(self, info: RoundInfo, cards: List[Card]) -> Action:
        curr_street = info.street_info[info.current_street]
        if curr_street.max_bet == 0:
            return Action(A.CHECK, 0, self.id)
        else:
            return Action(A.CALL, curr_street.max_bet, self.id)

    def log(self, info: RoundRecord):
        return