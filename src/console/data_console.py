from typing import List

from src.console.pretty_printer import PrettyPrinter
from src.data.base_data_store import BaseDataStore


class DataConsole:
    data_stores: List[BaseDataStore]

    def __init__(self, data_stores: List[BaseDataStore]):
        self.pretty_printer = PrettyPrinter()
        self.data_stores = data_stores

    def print_menu(self):
        print("Options: ")
        for i in range(len(self.data_stores)):
            print("%d - %s" % (i, self.data_stores[i]))
        print()

    def start_data_console(self):
        self.print_menu()
        while True:
            print('Input a command or type o for options again: ')
            command = input()
            if command == 'o':
                self.print_menu()
            elif command.isdigit():
                if int(command) < len(self.data_stores):
                    self.data_stores[int(command)].handle_console()
