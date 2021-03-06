# game phase is a global number describing what phase of the game we're in
# currently this is as follows:
# 0 - Nothing. Bot doesn't do anything really
# 1 - Signups. Bot serves signup requests but the game is not in progress
# 2 - in-game. CCs available, polls available, etc. Signups closed.

# use game_phase() to get the current game phase, and set_game_phase(new) to set it.
# GamePhases is an enum for convienience.
# needs_game_phase is a commands check that will only work in a certain game phase.

import discord
from discord.ext import commands

from wwbot.config import conf
import wwbot.errors
import atexit
from enum import IntEnum

GAMEPHASE_PATH = conf['database']['gamephase_filename']

class GamePhases(IntEnum):
    # convienience enum
    NOTHING = 0
    SIGNUP = 1
    GAME = 2

def _load_game_phase():
    try:
        with open(GAMEPHASE_PATH, "r") as fp:
            return int(fp.read().strip())
    except FileNotFoundError:
        return 0 # sensible default

@atexit.register
def _save_game_phase():
    with open(GAMEPHASE_PATH, "w") as fp:
        fp.write(str(__GAME_PHASE))

__GAME_PHASE = _load_game_phase()

def game_phase():
    return __GAME_PHASE

def set_game_phase(new):
    global __GAME_PHASE
    try:
        real_new = int(new)
        gp_new = GamePhases(real_new)
    except ValueError as e:
        raise ValueError("Invalid game phase: must be integer, must be valid game phase") from e
    __GAME_PHASE = gp_new.value

def needs_game_phase(gp):
    def predicate(ctx):
        current = game_phase()
        if current != gp:
            raise wwbot.errors.WrongGamePhase(gp, current)
        else:
            return True
    return commands.check(predicate)
