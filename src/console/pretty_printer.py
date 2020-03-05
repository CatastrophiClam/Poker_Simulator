from src.common.enums.action_type import ActionType
from src.common.enums.street import Street
from src.common.models.data import RoundRecord
from src.common.models.game import Action

"""
A collection of methods to pretty print stuff
"""
class PrettyPrinter:

    """
    Print one players action
    """
    @staticmethod
    def print_action(action: Action):
        if action.action == ActionType.CHECK:
            print('Player %s checks' % action.player_id)
        elif action.action == ActionType.CALL:
            print('Player %d calls %d' % (action.player_id, action.bet))
        elif action.action == ActionType.RAISE:
            print('Player %d raises, betting %d' % (action.player_id, action.bet))
        elif action.action == ActionType.FOLD:
            print('Player %d folds' % action.player_id)

    """
    Print the actions of one game
    """
    @staticmethod
    def print_round(round_number: int, record: RoundRecord):
        print('================== Round %s ===================' % round_number)
        print("Dealer: Player %d Blinds: %d %d" % (record.dealer, record.big_blind//2, record.big_blind))

        players_cards_string = ""
        for player in record.player_cards:
            players_cards_string += "Player {0}: {1} ".format(player, record.player_cards[player])
        print(players_cards_string)

        print()
        print('----PREFLOP----')
        [PrettyPrinter.print_action(i) for i in record.street_record[Street.PREFLOP].actions]
        print()
        if Street.FLOP in record.street_record:
            print('------FLOP-----')
            print("Flop comes %s" % record.community_cards[0:3])
            [PrettyPrinter.print_action(i) for i in record.street_record[Street.FLOP].actions]
            print()
        if Street.TURN in record.street_record:
            print('------TURN------')
            print("Turn is %s, board is now: %s" % (record.community_cards[3], record.community_cards[0:4]))
            [PrettyPrinter.print_action(i) for i in record.street_record[Street.TURN].actions]
            print()
        if Street.RIVER in record.street_record:
            print('-----RIVER-----')
            print("River is %s, board is now: %s" % (record.community_cards[4], record.community_cards[0:5]))
            [PrettyPrinter.print_action(i) for i in record.street_record[Street.RIVER].actions]
            print()

        for player in record.winners_to_winnings:
            if record.winners_to_winnings[player] > 0:
                print("Player %d wins %d with %s" %
                      (player, record.winners_to_winnings[player], record.player_cards[player]))
