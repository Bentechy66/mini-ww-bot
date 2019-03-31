# misc utility functions
import discord
from discord.ext import commands

import emoji
from wwbot.config import conf

import asyncio

def is_emoji_str(s):
    # returns whether s is a string containing nothing but a single emoji
    er = emoji.get_emoji_regexp()
    return len(s) == 1 and er.match(s)

def fetch_guild(bot):
    return discord.utils.get(bot.guilds, id=conf['ids'].getint('guild'))

def chunks(source, length):
    # yields successive n-sized chunks from l
    for i in range(0, len(source), length):
        yield source[i : i+length]

async def confirm(ctx, message="This is a dangerous operation!", timeout=10.0):
    # makes sure a human types "ok" in a channel
    # returns true if successful
    def check(m):
        return m.author.id == ctx.author.id and m.content.lower() == "ok" and m.channel == ctx.channel
    
    await ctx.send("{}\n*Please type 'ok' here to confirm. This will expire in {} seconds.*".format(message, timeout))
    try:
        msg = await ctx.bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.send("Timed out.")
        return False
    else:
        return True

