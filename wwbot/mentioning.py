# referring to people by emojis

import discord
from discord.ext import commands

from wwbot.db import Player

class PlayerConverter(commands.MemberConverter):
    async def convert(self, ctx, arg):
        player = Player.get_or_none(Player.emoji == arg)
        if player is None:
            return await super().convert(ctx, arg)
        else:
            return ctx.guild.get_member(player.discord_id)
