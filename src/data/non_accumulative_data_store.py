from abc import abstractmethod
from typing import List

from src.common.models.data import RoundRecord
from src.data.base_data_store import BaseDataStore
from src.data.base_filter import BaseFilter


class NonAccumulativeDataStore(BaseDataStore):

    def __init__(self, filters: List[BaseFilter]):
        super().__init__(filters)

    def handle_console(self):
        if len(self.filters) > 0:
            while True:
                print("Available filters: ")
                for i in range(len(self.filters)):
                    print("%d - " + self.filters[i] % i + 1)
                print()
                print("c - Clear filter")
                print("p - Print data")
                print("q - Back")
                print()
                print("Enter command: ")
                command = input()
                if command == 'p':
                    self.print_data()
                elif command == 'c':
                    self.clear_filters()
                elif command == 'q':
                    break
                elif command.isdigit():
                    command = int(command)
                    if command - 1 < len(self.filters):
                        self.use_filter(self.filters[command - 1])
                        print("Using filter: %s" % str(self.filters[command - 1]))
                    else:
                        print("Invalid filter")
                    print()
        else:
            self.print_data()

    def use_filter(self, filter_ind: int):
        self.segment_to_display = self.data_segments[filter_ind]

    @abstractmethod
    def record_segment(self, data_segment, record: RoundRecord) -> bool:
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def print_data(self):
        pass

    @abstractmethod
    def initialize_segment(self, segment):
        pass
