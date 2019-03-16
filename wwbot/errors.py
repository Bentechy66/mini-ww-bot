import discord
from discord.ext import commands

from wwbot.game_phase import GamePhases

class WWBotException(commands.CommandError):
    """base exception for all wwbot stuff"""
    def __str__(self):
        if self.__doc__ is not None:
            return self.__doc__
        else:
            return super().__str__()

class NoSuchChannel(WWBotException):
    """Channel or category does not exist"""
    pass
class OwnerNotFound(WWBotException):
    """Could not find CC owner"""
    pass
class NotACc(WWBotException):
    """The requested channel is not a CC"""
    pass
class NotOwner(WWBotException):
    """You are not the owner of this CC"""
    pass
class EmojiInUse(WWBotException):
    """That emoji is already being used"""
    pass

class WrongGamePhase(commands.CheckFailure, WWBotException):
    # wrong game phase.
    def __init__(self, needs, current):
        self.needs = GamePhases(needs)
        self.current = GamePhases(current)
    def __str__(self):
        fstr = "Wrong game phase! We needed `{0.name}` ({0.value}) but instead we are on `{1.name}` ({1.value})."
        return fstr.format(self.needs, self.current)

class NoSuchPoll(WWBotException):
    """That poll doesn't exist."""
    pass
class NeedsGM(commands.CheckFailure, WWBotException):
    """You need to be a Game Master to do that."""
    pass
class NeedsParticipant(commands.CheckFailure, WWBotException):
    """you need to be a participant"""
    pass
class NeedsGmChannel(commands.CheckFailure, WWBotException):
    """That command needs to be run in a GM Channel! (Add the word GMSAFE to a channel's topic to
    make it a GM channel.)
    """
    pass
