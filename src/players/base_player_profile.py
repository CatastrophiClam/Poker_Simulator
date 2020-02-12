from abc import ABC, abstractmethod
from typing import Tuple

from src.common.models.game import RoundInfo, Action
from src.common.enums.card import Card


class BasePlayerProfile(ABC):
    id = -1

    def set_self_id(self, id):
        self.id = id

    @abstractmethod
    def respond(self, round_info: RoundInfo, cards: Tuple[Card, Card]) -> Action:
        pass
