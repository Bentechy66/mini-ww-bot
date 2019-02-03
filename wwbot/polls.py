import discord
from discord.ext import commands

from wwbot.util import fetch_guild, chunks
from wwbot.db import Player, Poll, PollMessage
from wwbot.permissions import is_participant
from wwbot import errors

def get_all_alive(bot):
    guild = fetch_guild(bot)
    alive = []
    for p in Player.select():
        m = guild.get_member(p.discord_id)
        if is_participant(m):
            alive.append(p)
    return alive

async def create_poll(ch, options):
    # options should have properties discord_id and emoji
    poll = Poll.create(channel=ch.id)
    await ch.send("Poll #`{}`".format(poll.id))
    for chunk in chunks(options, 1):
        # chunk is a list of 20 Players from db
        pollmsg = await ch.send("\n".join("{0.emoji} - <@{0.discord_id}>".format(opt) for opt in chunk))
        PollMessage.create(poll=poll, discord_id=pollmsg.id)
        for p in chunk:
            await pollmsg.add_reaction(p.emoji)

async def close_poll(bot, pollid):
    guild = fetch_guild(bot)
    me = guild.me
    poll = Poll.get_or_none(id=pollid)
    if poll is None:
        raise errors.NoSuchPoll()
    reactions = {}
    channel = bot.get_channel(poll.channel)
    for dbmsg in poll.messages:
        msg = await channel.get_message(dbmsg.discord_id)
        for reaction in msg.reactions:
            users = await reaction.users().flatten()
            users.remove(me)
            reactions[reaction.emoji] = users
        await msg.clear_reactions()
    poll.delete_instance(recursive=True)
    return reactions
