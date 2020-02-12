from src.data.pretty_printer import PrettyPrinter


class DataTracker:

    PP = PrettyPrinter()

    saved_games = []
    should_log_all_rounds = False

    def __init__(self, should_log_all_rounds):
        self.should_log_all_rounds = should_log_all_rounds

    def log(self, info):
        if self.should_log_all_rounds:
            entry = {
                'game_actions': info['game_actions'],
                'cards': info['cards'],
                'player_hands': info['player_hands'],
            }
            self.saved_games.append(entry)

    def print_game(self, game_number):
        game = self.saved_games[game_number]
        self.PP.print_game(game_number, game['game_actions'])

    def start_analytics(self):
        while True:
            print('Input a command or type help for a list of commands: ')
            command = input()
            if command == help:
                self.PP.print_menu()
            elif command.startswith('game'):
                c = command.split(' ')
                self.print_game(int(c[1]))
            elif command == 'quit':
                break
