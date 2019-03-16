# actual discord stuff
import discord
from discord.ext import commands

from wwbot.config import conf
from wwbot import errors
from wwbot.util import fetch_guild
from wwbot.db import CCCategory

import random

def fetch_cc_category_ids():
    ret = []
    for cat in CCCategory.select():
        ret.append(cat.discord_id)
    return ret

async def fetch_a_category(bot):
    ids = fetch_cc_category_ids()
    guild = fetch_guild(bot)
    for catid in ids:
        cat = guild.get_channel(catid)
        if cat is None:
            CCCategory.get(discord_id=catid).delete_instance()
            continue # clean up and skip if it no longer exists
        if len(cat.text_channels) < 30:
            return cat
            break
    return await create_new_category(bot)

async def create_new_category(bot):
    guild = fetch_guild(bot)
    cat = await guild.create_category_channel("More CCs rename me")
    CCCategory.create(discord_id=cat.id)
    return cat

def is_cc(channel):
    # is that channel a cc?
    # we see if it's in one of the cc categories.
    categories = fetch_cc_category_ids()
    return channel.category_id in categories

def get_cc_owner(channel):
    if not is_cc(channel):
        raise errors.NotACc()
    for target, ows in channel.overwrites:
        if isinstance(target, discord.Member) and ows.read_message_history:
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
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        # dead: read, no send
        guild.get_role(conf['ids'].getint("dead")): discord.PermissionOverwrite(read_messages=True, send_messages=False),
        # spectator: read, no send
        guild.get_role(conf['ids'].getint("spectator")): discord.PermissionOverwrite(read_messages=True, send_messages=False),
        # gamemasters: read, send
        guild.get_role(conf['ids'].getint("gamemaster")): discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    for person in people:
        # person will be a member
        overwrites[person] = discord.PermissionOverwrite(read_messages=True)
    overwrites[owner].read_message_history = True # they would have this anyway so we use it to store the owner
    return overwrites

async def create_cc(bot,name,owner,people,hidden=False,category=None):
    # people should contain owner
    if owner not in people:
        people.append(owner)
    
    guild = fetch_guild(bot)
    if category is None:
        category = await fetch_a_category(bot)
    if category is None: raise errors.NoSuchChannel()

    overwrites = get_overwrites(guild, people, owner)
    channel = await guild.create_text_channel(
        name,
        overwrites=overwrites,
        category=category
    )

    people_mentions = [p.mention for p in people]
    random.shuffle(people_mentions)
    
    if hidden:
        msg = "A new CC has been created!\n**Members:**\n{}".format("\n".join(people_mentions))
    else:
        msg = "{} has created a new CC!\n**Members:**\n{}".format(owner.mention,"\n".join(people_mentions))
    await channel.send(msg)

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
