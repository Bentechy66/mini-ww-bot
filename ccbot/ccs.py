# actual discord stuff
import discord
from discord.ext import commands

from config import conf
import errors

def fetch_guild(bot):
    return discord.utils.get(bot.guilds, id=conf['ids'].getint('guild'))

def fetch_category(bot):
    return fetch_guild(bot).get_channel(conf['ids'].getint('category'))

def is_cc(guild,channel):
    pass # is that channel a cc?

def get_cc_owner(channel):
    for target, ows in channel.overwrites:
        if isinstance(target, discord.Member) and ows.send_messages:
            return target
    raise errors.OwnerNotFound()

def get_cc_people(channel):
    pass # get all people in a cc including owner

def get_overwrites(guild,people,owner):
    overwrites = {
        # @everyone: no read
        # each person: read
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    for person in people:
        # person will be a member
        overwrites[person] = discord.PermissionOverwrite(read_messages=True)
    overwrites[owner].send_messages = True # they would have this anyway so we use it to store the owner
    return overwrites

async def create_cc(bot,name,owner,people):
    # people should contain owner
    if owner not in people:
        people.append(owner)
    
    guild = fetch_guild(bot)
    category = fetch_category(bot)
    if category is None: raise errors.NoSuchChannel()

    overwrites = get_overwrites(guild, people, owner)
    channel = await guild.create_text_channel(
        name,
        overwrites=overwrites,
        category=category
    )
    await channel.send("TODO: cc message")

