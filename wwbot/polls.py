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
    for chunk in chunks(options, 20):
        # chunk is a list of 20 Players from db
        pollmsg = await ch.send("\n".join("{0.emoji} - <@{0.discord_id}>".format(opt) for opt in chunk))
        PollMessage.create(poll=poll, discord_id=pollmsg.id)
        for p in chunk:
            await pollmsg.add_reaction(p.emoji)

