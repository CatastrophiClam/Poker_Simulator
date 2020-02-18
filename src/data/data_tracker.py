from typing import List

from src.common.models.data import RoundRecord
from src.data.base_data_store import BaseDataStore


class DataTracker:
    persistent_log_threshold = -1
    data_stores: List[BaseDataStore]

    def __init__(self, persistent_log_threshold, data_stores: List[BaseDataStore]):
        self.persistent_log_threshold = persistent_log_threshold
        self.data_stores = data_stores

    """
    :return True if all data_stores recorded data successfully, otherwise false
    """
    def log(self, info: RoundRecord):
        successful = True
        for store in self.data_stores:
            successful = successful and store.record(info)
        return successful
