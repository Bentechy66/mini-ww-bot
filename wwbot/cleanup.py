# various commands for doing cleanup stuff

import discord
from discord.ext import commands

from wwbot.util import fetch_guild, confirm
from wwbot.permissions import chk_gamemaster, chk_gm_channel
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot.db import CCCategory, Player
from wwbot.config import conf

class CleanupCmds(commands.Cog, name="Cleanup"):
    def __init__(self, bot):
        self.bot=bot
        self.guild = fetch_guild(self.bot)

    @chk_gamemaster()
    @chk_gm_channel()
    @needs_game_phase(GamePhases.NOTHING)
    @commands.group()
    async def cleanup(self, ctx):
        """Container group for all the cleanup commands"""
        pass
    
    @cleanup.command()
    async def ccs(self, ctx):
        """Delete all cc channels and categories, purging them from the db too."""
        if await confirm(ctx, "All CC Channels will be deleted!"):
            for cat_mod in CCCategory.select():
                cat = self.guild.get_channel(cat_mod.discord_id)
                if cat is not None:
                    for ch in cat.text_channels:
                        await ch.delete()
                    await cat.delete()
                cat_mod.delete_instance()
            await ctx.send(":white_check_mark: Done")
    
    @cleanup.command()
    async def purgecat(self, ctx, cat: discord.CategoryChannel, also_delete_cat : bool = False):
        """Delete all messages in a category, and optionally delete the category itself too.
        
        Don't use this on CCs, use {PREFIX}cleanup ccs instead, otherwise you might break something."""
        msg = "All channels in category {} will be deleted".format(cat.name)
        if also_delete_cat:
            msg += ", as well as the category itself too"
        msg += "!"
        if await confirm(ctx, msg):
            for ch in cat.text_channels:
                await ch.delete()
            if also_delete_cat:
                await cat.delete()
            await ctx.send(":white_check_mark: Done")
    
    @cleanup.command()
    async def users(self, ctx):
        """Remove Participant, Dead Participant and Spectator roles from everyone, and then reset list of players.

        This doesn't affect the Mayor or Reporter roles, so you will still need to do that yourself.
        """
        if await confirm(ctx, "This will remove everyone's roles and end the game completely."):
            participant = self.guild.get_role(conf['ids'].getint("participant"))
            dead = self.guild.get_role(conf['ids'].getint("dead"))
            spec = self.guild.get_role(conf['ids'].getint("spectator"))
            for pl in Player.select():
                mem = self.guild.get_member(pl.discord_id)
                await mem.remove_roles(participant, dead, spec)
                await ctx.send(":white_check_mark: Processed {}".format(mem.mention))
            Player.delete().execute()
            await ctx.send(":white_check_mark: Player list cleared")

def setup(bot):
    bot.add_cog(CleanupCmds(bot))
