# secret channel creation stuff

import discord
from discord.ext import commands

from wwbot.util import fetch_guild
from wwbot.permissions import chk_gamemaster, chk_gm_channel
from wwbot.config import conf
from wwbot.ccs import create_cc
from wwbot.db import Player

class SecretChannelCmds(commands.Cog, name="Secret Channels"):
    def __init__(self, bot):
        self.bot = bot
        self.guild = fetch_guild(self.bot)
    
    async def create_secret_channel(self, name, people):
        # people should be a list of Member
        category = self.guild.get_channel(conf['ids'].getint('sc_category'))
        await create_cc(self.bot, name, None, people, category=category, announce=False)

    @chk_gamemaster()
    @chk_gm_channel()
    @commands.group()
    async def create_sc(self, ctx):
        """Group of commands for dealing with secret channels"""
        pass
    
    @create_sc.command()
    async def ind(self, ctx, role):
        """Creates individual secret channels for everybody with
        this role, separately."""
        for p in Player.select().where(Player.role == role):
            member = self.guild.get_member(p.discord_id)
            await self.create_secret_channel(role, [member])
        await ctx.send(":white_check_mark: Done!")

    @create_sc.command()
    async def multi(self, ctx, name, *roles):
        """Creates a single secret channel with every person with any of
        the specified role in. Remember to specify the name!"""
        players = Player.select().where(Player.role.in_(roles))
        await self.create_secret_channel(name, [self.guild.get_member(p.discord_id) for p in players])
        await ctx.send(":white_check_mark: Done!")



def setup(bot):
    bot.add_cog(SecretChannelCmds(bot))
