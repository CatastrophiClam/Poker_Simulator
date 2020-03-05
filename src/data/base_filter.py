from abc import ABC, abstractmethod

from src.common.models.data import RoundRecord


class BaseFilter(ABC):

    # return true if record passes filter
    @abstractmethod
    def check(self, record: RoundRecord):
        pass

    # Return description of categorizer fit for menu
    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()
