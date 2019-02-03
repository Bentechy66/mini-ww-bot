import discord
from discord.ext import commands

from wwbot.game_phase import game_phase, set_game_phase, GamePhases
from wwbot.permissions import chk_gamemaster

class GamePhaseCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def gamephase(self, ctx):
        """Returns the current game phase of the system."""
        await ctx.send("The current game phase is `{0.name}` ({0.value}).".format(GamePhases(game_phase())))

    @chk_gamemaster()
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

def setup(bot):
    bot.add_cog(GamePhaseCmds(bot))
