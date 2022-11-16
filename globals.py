# game
from datetime import datetime

active_game_index = 0
start_time = datetime.now()

def StartChallenge():
    global active_game_index, start_time
    active_game_index = 1
    start_time = datetime.now()

