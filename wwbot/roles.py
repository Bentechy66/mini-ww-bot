# keeps track of peoples roles
# does not do role abilities etc, that is beyond the scope of this bot.

import discord
from discord.ext import commands

from wwbot.db import Player
from wwbot.permissions import chk_gm_channel
from wwbot.util import fetch_guild

def everyone_has_a_role():
    # is everything in a state that means we can start the game yet?
    # (does everyone have a role?)
    return Player.select().where(Player.role == "").count() == 0

class RoleCmds(commands.Cog, name="Roles"):
    def __init__(self, bot):
        self.bot = bot

    @chk_gm_channel()
    @commands.command()
    async def get_all_roles(self, ctx):
        guild = fetch_guild(self.bot)
        r = []
        for p in Player.select():
            r.append("{m} - **{r}**".format(m=guild.get_member(p.discord_id).mention, r=p.role or "???"))
        await ctx.send("\n".join(r))
    
    @chk_gm_channel()
    @commands.command()
    async def set_role(self, ctx, who: discord.Member, role: str = ""):
        p = Player.get(Player.discord_id == who.id)
        p.role = role
        p.save()
        if role == "":
            await ctx.send(":white_check_mark: cleared {}'s role".format(who.mention))
        else:
            await ctx.send(":white_check_mark: {}'s role set to **{}**".format(who.mention, role))
    
    @chk_gm_channel()
    @commands.command()
    async def _t_rts(self, ctx):
        await ctx.send(str(everyone_has_a_role()))

def setup(bot):
    bot.add_cog(RoleCmds(bot))
