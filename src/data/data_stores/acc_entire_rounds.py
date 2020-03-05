from typing import List

from src.common.models.data import RoundRecord
from src.console.pretty_printer import PrettyPrinter
from src.data.accumulative_data_store import AccumulativeDataStore
from src.data.base_filter import BaseFilter


class AccEntireRounds(AccumulativeDataStore):

    def __init__(self, filters: List[BaseFilter]):
        super().__init__(filters)

    def initialize_segment(self, segment, is_segment_unfiltered_segment=False):
        if is_segment_unfiltered_segment:
            segment['rounds'] = []
        else:
            segment['rounds'] = set()

    def record_segment(self, data_segment, is_segment_unfiltered_segment: bool, record: RoundRecord) -> bool:
        if is_segment_unfiltered_segment:
            data_segment['rounds'].append(record)
        else:
            data_segment['rounds'].add(self.total_games_recorded)

    def apply_filters(self):
        new_segment = {'rounds': []}
        for i in range(len(self.unfiltered_segment['rounds'])):
            add_round = True
            for filter_ind in self.filters_active:
                in_inv_filter = (filter_ind < 0 and i in self.data_segments[abs(filter_ind)-1]['rounds'])
                not_in_filter = (filter_ind > 0 and i not in self.data_segments[filter_ind-1]['rounds'])
                if in_inv_filter or not_in_filter:
                    add_round = False
                    break
            if add_round:
                new_segment['rounds'].append(self.unfiltered_segment['rounds'][i])
        self.segment_to_display = new_segment

    def print_data(self):
        while True:
            print("%d rounds found." % len(self.segment_to_display['rounds']))
            print("Enter round number to print round")
            print("all - print all rounds")
            print("q - back")
            command = input()
            if command == 'all':
                for record in self.segment_to_display['rounds']:
                    PrettyPrinter.print_round(record)
            elif command == 'q':
                break
            elif command.isdigit():
                command = int(command)
                if command < len(self.segment_to_display['rounds']):
                    PrettyPrinter.print_round(command, self.segment_to_display['rounds'][command])
                else:
                    print("Invalid round")
            print()

    def __str__(self):
        return "Entire rounds of poker from beginning to end"
