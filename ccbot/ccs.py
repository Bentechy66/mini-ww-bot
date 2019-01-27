# actual discord stuff
import discord
from discord.ext import commands

from config import conf
import errors

def fetch_guild(bot):
    return discord.utils.get(bot.guilds, id=conf['ids'].getint('guild'))

def fetch_category(bot):
    return fetch_guild(bot).get_channel(conf['ids'].getint('category'))

def is_cc(channel):
    # is that channel a cc?
    # for now we see if it's in the ccs category.
    # this may change later
    return channel.category_id == conf['ids'].getint('category')

def get_cc_owner(channel):
    if not is_cc(channel):
        raise errors.NotACc()
    for target, ows in channel.overwrites:
        if isinstance(target, discord.Member) and ows.send_messages:
            return target
    raise errors.OwnerNotFound()

def get_cc_people(channel):
    # returns list of member who are in cc (includes owner)
    if not is_cc(channel):
        raise errors.NotACc()
    res = []
    for target, perms in channel.overwrites:
        if isinstance(target, discord.Member):
            allow, deny = perms.pair()
            if allow.read_messages:
                res.append(target)
    return res

def check_cc_owner(ctx):
    # not using ext.commands checks because that effects the help system
    owner = get_cc_owner(ctx.channel)
    if ctx.author != owner:
        raise errors.NotOwner()

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

async def add_to_cc(channel, people):
    if not is_cc(channel):
        raise errors.NotACc()
    changed = []
    current_people = get_cc_people(channel)
    for person in people:
        if person in current_people:
            continue
        await channel.set_permissions(person, read_messages=True)
        changed.append(person)
    return changed

async def remove_from_cc(channel, people):
    if not is_cc(channel):
        raise errors.NotACc()
    changed = []
    current_people = get_cc_people(channel)
    owner = get_cc_owner(channel)
    for person in people:
        if person not in current_people:
            continue
        if person == owner:
            continue # can't remove owner
        await channel.set_permissions(person, overwrite=None)
        changed.append(person)
    return changed
