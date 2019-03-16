# keeps track of peoples roles
# does not do role abilities etc, that is beyond the scope of this bot.

import discord
from discord.ext import commands

from wwbot.db import Player
from wwbot.permissions import chk_gm_channel, chk_gamemaster
from wwbot.util import fetch_guild
from wwbot.config import conf

def everyone_has_a_role():
    # is everything in a state that means we can start the game yet?
    # (does everyone have a role?)
    return Player.select().where(Player.role == "").count() == 0

class RoleCmds(commands.Cog, name="Roles"):
    def __init__(self, bot):
        self.bot = bot
        self.guild = fetch_guild(self.bot)
    
    async def send_role_to(self, player):
        member = self.guild.get_member(player.discord_id)
        msg = conf['general']['role_message'].format(role=player.role)
        await member.send(msg)

    @chk_gm_channel()
    @chk_gamemaster()
    @commands.group()
    async def roles(self, ctx):
        pass

    @roles.command()
    async def send(self, ctx):
        for p in Player.select():
            await ctx.send("Sending role to {}".format(self.guild.get_member(p.discord_id)))
            await self.send_role_to(p)
        await ctx.send(":white_check_mark: Done")

    @roles.command(name="list")
    async def _list(self, ctx):
        guild = self.guild
        r = []
        for p in Player.select():
            r.append("{m} - **{r}**".format(m=guild.get_member(p.discord_id).mention, r=p.role or "???"))
        await ctx.send("\n".join(r))
    
    @roles.command(name="set")
    async def _set(self, ctx, who: discord.Member, role: str = ""):
        p = Player.get(Player.discord_id == who.id)
        p.role = role
        p.save()
        if role == "":
            await ctx.send(":white_check_mark: cleared {}'s role".format(who.mention))
        else:
            await ctx.send(":white_check_mark: {}'s role set to **{}**".format(who.mention, role))
    

def setup(bot):
    bot.add_cog(RoleCmds(bot))
