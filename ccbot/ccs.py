# actual discord stuff
import discord
from discord.ext import commands

from config import conf
import errors

def get_basic_overwrites(guild):
    BASIC_OVEWRITES = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    return BASIC_OVEWRITES

async def create_cc(bot,name,owner,people):
    # people should not contain owner
    guild = discord.utils.get(bot.guilds, id=conf['general'].getint('guild_id'))
    category = guild.get_channel(conf['general'].getint('category_id'))
    if category is None: raise errors.NoSuchChannel()
    overwrites = get_basic_overwrites(guild)
    channel = await guild.create_text_channel(
        name,
        overwrites=overwrites,
        category=category
    )
    await channel.send("Hi!!")

