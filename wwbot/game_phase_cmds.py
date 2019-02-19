import discord
from discord.ext import commands

from wwbot.game_phase import game_phase, set_game_phase, GamePhases
from wwbot.permissions import chk_gamemaster
from wwbot.db import Player
from wwbot.util import fetch_guild
from wwbot.config import conf

class GamePhaseCmds:
    def __init__(self, bot):
        self.bot = bot

    @chk_gamemaster()
    @commands.group(invoke_without_command=True)
    async def gamephase(self, ctx):
        """Returns the current game phase of the system."""
        await ctx.send("The current game phase is `{0.name}` ({0.value}).".format(GamePhases(game_phase())))

    @gamephase.command()
    async def set(self, ctx, to):
        """Sets the current game phase to either an int or a word."""
        try:
            int_to = int(to)
        except ValueError:
            try:
                int_to = int(GamePhases[to].value)
            except KeyError:
                await ctx.send("{} is not a valid game phase.".format(to))
                return
        set_game_phase(int_to)
        await ctx.send(":white_check_mark: Game Phase is now `{0.name}` ({0.value})".format(GamePhases(game_phase())))

    @chk_gamemaster()
    @commands.check(lambda _: game_phase() != GamePhases.GAME)
    @commands.command()
    async def start_game(self, ctx):
        """Assigns the participant role to all players and changes game phase.

        This is equivalent to manually assigning the Participant role to all
        signed up players, then doing `{PREFIX}gamephase set GAME`.
        """
        guild = fetch_guild(self.bot)
        participant = guild.get_role(conf['ids'].getint("participant"))
        for p in Player.select():
            m = guild.get_member(p.discord_id)
            await m.add_roles(participant)
            await ctx.send("{} is now a participant...".format(m.mention))
        set_game_phase(GamePhases.GAME)
        await ctx.send("Set game phase to `GAME` ({})".format(GamePhases.GAME.value))

def setup(bot):
    bot.add_cog(GamePhaseCmds(bot))
