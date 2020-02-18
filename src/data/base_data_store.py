from abc import ABC, abstractmethod

from src.common.models.data import RoundRecord

"""
Stores a specific metric we want to measure for each session
"""
class BaseDataStore(ABC):

    @abstractmethod
    def record(self, round_record: RoundRecord) -> bool:
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def handle_console_queries(self):
        pass
