from abc import abstractmethod
from typing import List

from src.common.models.data import RoundRecord
from src.data.base_data_store import BaseDataStore
from src.data.base_filter import BaseFilter


class AccumulativeDataStore(BaseDataStore):

    def __init__(self, filters: List[BaseFilter]):
        super().__init__(filters)
        # NOTE this stores the index + 1 of all the active filters
        self.filters_active = []

    def handle_console(self):
        if len(self.filters) > 0:
            while True:
                print("Available filters - use number to select filter or negative of number to select inverse filter")
                for i in range(len(self.filters)):
                    print(("%d - "+str(self.filters[i])) % (i+1))
                print()
                print("c - Clear filters")
                print("p - Print data")
                print("q - Back")
                print()
                print("Enter command: ")
                command = input()
                if command == 'p':
                    self.apply_filters()  # Only apply all filters before printing
                    self.print_data()
                elif command == 'c':
                    self.clear_filters()
                elif command == 'q':
                    break
                elif command.lstrip('-+').isdigit():
                    command = int(command)
                    print(command)
                    if command < 0:
                        if abs(command) - 1 < len(self.filters):
                            self.add_inverse_filter(command)
                            print("Applied inverse of %s" % str(self.filters[abs(command) - 1]))
                        else:
                            print("Invalid filter")
                    else:
                        if command - 1 < len(self.filters):
                            self.add_filter(command)
                            print("Applied %s" % str(self.filters[command - 1]))
                        else:
                            print("Invalid filter")
                    print()
                else:
                    print("Invalid command")
        else:
            self.print_data()

    # NOTE: filter_index is one more than index of actual filter
    def add_filter(self, filter_chosen: int):
        if filter_chosen not in self.filters_active:
            self.filters_active.append(filter_chosen)

    # NOTE: abs(filter_index) is one more than index of actual filter
    def add_inverse_filter(self, filter_chosen: int):
        if filter_chosen not in self.filters_active:
            self.filters_active.append(filter_chosen)

    def clear_filters(self):
        self.filters_active = []
        self.segment_to_display = self.unfiltered_segment

    # Apply all active filters to unfiltered data to produce segment_to_display
    @abstractmethod
    def apply_filters(self):
        pass

    @abstractmethod
    def record_segment(self, data_segment, is_segment_unfiltered_segment: bool, record: RoundRecord) -> bool:
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def print_data(self):
        pass

    @abstractmethod
    def initialize_segment(self, segment, is_segment_unfiltered_segment=False):
        pass
