import discord
from discord.ext import commands

from wwbot.util import fetch_guild
from wwbot.db import Player
from wwbot.permissions import is_participant

def get_all_alive(bot):
    guild = fetch_guild(bot)
    alive = []
    for p in Player.select():
        m = guild.get_member(p.discord_id)
        if is_participant(m):
            alive.append(m)
    return alive
