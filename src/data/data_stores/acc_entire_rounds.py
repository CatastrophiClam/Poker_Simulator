from src.common.models.data import RoundRecord
from src.data.base_data_store import BaseDataStore


class AccEntireRounds(BaseDataStore):
    def initialize_segment(self, segment):
        pass

    def record_segment(self, data_segment, record: RoundRecord) -> bool:
        pass

    def handle_console(self):
        pass

    def print_data(self):
        pass

    def __str__(self):
        return "Entire rounds of poker from beginning to end"
