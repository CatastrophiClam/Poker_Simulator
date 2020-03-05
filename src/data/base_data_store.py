from abc import ABC, abstractmethod
from typing import List

from src.common.models.data import RoundRecord
from src.data.base_filter import BaseFilter

"""
Stores a specific metric we want to measure for each session
"""
class BaseDataStore(ABC):

    def __init__(self, filters: List[BaseFilter]):
        self.filters = filters
        self.total_games_recorded = 0
        self.data_segments = [{} for i in filters]
        self.unfiltered_segment = {}
        self.segment_to_display = self.unfiltered_segment

        for segment in self.data_segments:
            self.initialize_segment(segment)
        self.initialize_segment(self.unfiltered_segment, True)

    def record(self, record: RoundRecord) -> bool:
        answer = True
        for i in range(len(self.filters)):
            if self.filters[i].check(record):
                answer = answer and self.record_segment(self.data_segments[i], False, record)
        answer = answer and self.record_segment(self.unfiltered_segment, True, record)

        # Make sure total games recorded is incremented AFTER all segments have recorded data
        self.total_games_recorded += 1
        return answer

    def clear_filters(self):
        self.segment_to_display = self.unfiltered_segment

    # Initialize empty segment
    @abstractmethod
    def initialize_segment(self, segment, is_segment_unfiltered_segment=False):
        pass

    # Record data from record to a certain segment
    @abstractmethod
    def record_segment(self, data_segment, is_segment_unfiltered_segment: bool, record: RoundRecord) -> bool:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    # Handler for when console transfers control to current data store
    @abstractmethod
    def handle_console(self):
        pass

    # Print data taking into account the filters chosen
    @abstractmethod
    def print_data(self):
        pass
