from src.game.session import Session
from src.players.player import Player
from src.data.data import DataTracker
from src.players.ai.profiles.v0.profile import PlayerProfile as ProfileV0
from src.common.enums.card import Card as C

NUM_HANDS_PER_SESSION = 1000
STARTING_MONEY = 100000
BIG_BLIND = 500
LOG_THRESHOLD = 1000000

# MAIN SCRIPT
# generate players
player_profiles = [ProfileV0(), ProfileV0(), ProfileV0(), ProfileV0()]
players = [Player(player_profiles[i], STARTING_MONEY, i) for i in range(len(player_profiles))]

should_log_all_games = True
if NUM_HANDS_PER_SESSION > LOG_THRESHOLD:
    should_log_all_games = False

data = DataTracker(should_log_all_games)

# Create session
session = Session(players, BIG_BLIND, STARTING_MONEY)
# session.set_deck_biases({0: (C.SA, C.H2), 1: (C.HA, C.S7), 2: (C.DA, C.S5), 3: (C.S2, C.H7)})
# session.set_com_cards([C.C3, C.S3, C.S4, C.H4, C.HK])

# run game NUM_TRIALS times
for i in range(NUM_HANDS_PER_SESSION):
    info = session.run_round()
    # data.log(info)

for i in players:
    print("Player %d has %d chips out of a %d investment" % (i.id, i.money, i.total_money_invested))
# data.start_analytics()
