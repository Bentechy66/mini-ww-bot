import discord
from discord.ext import commands

from wwbot.game_phase import GamePhases

class NoSuchChannel(Exception):
    # channel or category does not exist
    pass
class OwnerNotFound(Exception):
    # could not find cc owner
    pass
class NotACc(Exception):
    # the requested channel is not a CC
    pass
class NotOwner(commands.CommandError):
    # you are not the owner of this cc
    pass
class EmojiInUse(Exception):
    # that emoji is already being used
    pass

class WrongGamePhase(commands.CheckFailure):
    # wrong game phase.
    def __init__(self, needs, current):
        self.needs = GamePhases(needs)
        self.current = GamePhases(current)
    def __str__(self):
        fstr = "Wrong game phase! We needed `{0.name}` ({0.value}) but instead we are on `{1.name}` ({1.value})."
        return fstr.format(self.needs, self.current)

class PermissionsError(Exception):
    # base exeption for permission-related stuff
    pass
class NeedsGM(PermissionError):
    # you need to be a gamemaster to do that
    pass
class NeedsParticipant(PermissionError):
    # you need to be a participant
    pass
