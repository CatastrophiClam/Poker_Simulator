from src.common.enums import action_type as A

"""
A collection of methods to pretty print stuff
"""
class PrettyPrinter:

    def convert_game_actions_to_streets(self, game_actions):
        preflop_actions = []
        flop_actions = []
        turn_actions = []
        river_actions = []

        ind = 0
        current_action = game_actions[0]
        while (current_action['action'] != A.NEXT_ROUND):
            preflop_actions.append(current_action)
            ind += 1
            current_action = game_actions[ind]

        ind += 1
        current_action = game_actions[ind]
        while (current_action['action'] != A.NEXT_ROUND):
            flop_actions.append(current_action)
            ind += 1
            current_action = game_actions[ind]

        ind += 1
        current_action = game_actions[ind]
        while (current_action['action'] != A.NEXT_ROUND):
            turn_actions.append(current_action)
            ind += 1
            current_action = game_actions[ind]

        ind += 1
        current_action = game_actions[ind]
        while (current_action['action'] != A.NEXT_ROUND):
            river_actions.append(current_action)
            ind += 1
            current_action = game_actions[ind]

        return {
            'preflop_actions': preflop_actions,
            'flop_actions': flop_actions,
            'turn_actions': turn_actions,
            'river_actions': river_actions,
        }

    """
    Print analytics menu
    """
    def print_menu(self):
        print('game [int]       - pretty print a game')

    """
    Print one players action
    """
    def print_action(self, action):
        if action['action'] == A.CHECK:
            print('Player %s checks' % action['players'])
        elif action['action'] == A.CALL:
            print('Player %d calls, betting %d' % (action['players'], action['bet']))
        elif action['action'] == A.RAISE:
            print('Player %d raises, betting %d' % (action['players'], action['bet']))
        elif action['action'] == A.FOLD:
            print('Player %d folds' % action['players'])

    """
    Print the actions of one game
    """
    def print_game(self, game_number, game_actions):
        actions = self.convert_game_actions_to_streets(game_actions)
        
        print('================== GAME %s ===================' % game_number)
        print()
        print('----PREFLOP----')
        [self.print_action(i) for i in actions['preflop_actions']]
        print()
        print('------FLOP-----')
        [self.print_action(i) for i in actions['flop_actions']]
        print()
        print('------TURN------')
        [self.print_action(i) for i in actions['turn_actions']]
        print()
        print('-----RIVER-----')
        [self.print_action(i) for i in actions['river_actions']]
        print()