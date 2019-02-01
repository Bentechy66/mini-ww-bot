# misc utility functions
import discord
from discord.ext import commands

import emoji
from wwbot.config import conf

def is_emoji_str(s):
    # returns whether s is a string containing nothing but a single emoji
    er = emoji.get_emoji_regexp()
    return len(s) == 1 and er.match(s)

def fetch_guild(bot):
    return discord.utils.get(bot.guilds, id=conf['ids'].getint('guild'))
