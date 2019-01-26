import discord
from discord.ext import commands

class NoSuchChannel(Exception):
    pass
class OwnerNotFound(Exception):
    pass
class NotACc(Exception):
    pass
