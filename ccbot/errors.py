import discord
from discord.ext import commands

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
