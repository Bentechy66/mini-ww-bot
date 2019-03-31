# referring to people by emojis

import discord
from discord.ext import commands

from wwbot.db import Player
from wwbot.permissions import is_participant

class PlayerConverter(commands.MemberConverter):
    def __init__(self, needs_alive=True):
        super().__init__()
        self.needs_alive = needs_alive
    
    async def convert(self, ctx, arg):
        player = Player.get_or_none(Player.emoji == arg)
        if player is None:
            member =  await super().convert(ctx, arg)
        else:
            member = ctx.guild.get_member(player.discord_id)
        if not self.needs_alive:
            return member
        if is_participant(member):
            return member
        else:
            raise commands.BadArgument("{} is not a living participant!".format(member.display_name))

