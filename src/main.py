from src.console.data_console import DataConsole
from src.data.data_stores.players_games_and_money_won import PlayersGamesAndMoneyWon
from src.game.session import Session
from src.players.player import Player
from src.data.data_tracker import DataTracker
from src.players.ai.profiles.v0.profile import PlayerProfile as ProfileV0
from src.common.enums.card import Card as C

NUM_HANDS_PER_SESSION = 10000
STARTING_MONEY = 100000
BIG_BLIND = 500
PERSISTENT_LOG_THRESHOLD = 50000

# MAIN SCRIPT
# generate players
player_profiles = [ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0()]
players = [Player(player_profiles[i], STARTING_MONEY, i) for i in range(len(player_profiles))]

# Data stuff
data_stores = [PlayersGamesAndMoneyWon()]
data_tracker = DataTracker(PERSISTENT_LOG_THRESHOLD, data_stores)

# Create session
session = Session(players, BIG_BLIND, STARTING_MONEY)
# session.set_deck_biases({0: (C.SA, C.H2), 1: (C.HA, C.S7), 2: (C.DA, C.S5), 3: (C.S2, C.H7)})
# session.set_com_cards([C.C3, C.S3, C.S4, C.H4, C.HK])

# run game NUM_TRIALS times
for i in range(NUM_HANDS_PER_SESSION):
    info = session.run_round()
    for player in players:
        if player.money < STARTING_MONEY / 2:
            player.rebuy()
    data_tracker.log(info)

# Start data console
data_console = DataConsole(data_stores)
data_console.start_data_console()
