import discord
from discord.ext import commands

from wwbot.permissions import chk_gamemaster
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot import polls

class PollCmds(commands.Cog, name="Polls"):
    def __init__(self, bot):
        self.bot = bot

    @needs_game_phase(GamePhases.GAME)
    @chk_gamemaster()
    @commands.group()
    async def poll(self, ctx):
        """All commands to do with polls.

        These are all gamemaster-only
        """
        pass
    
    @poll.command()
    async def new(self, ctx):
        """Create a new poll in the current channel.

        All of the currently alive players will be options for voting.
        """
        # creates a poll with options of all alive players for voting for everyone in this channel.
        await polls.create_poll(ctx.channel, polls.get_all_alive(self.bot))
    
    @poll.command()
    async def close(self, ctx, pollid : int):
        """Close any open poll and print the raw results in the current channel.

        pollid should be the id of the poll that was given to you by the ]poll new command.
        This doesn't have to be run in the same channel that the poll was created in.
        """
        # closes that poll, puts results somewhere
        result = await polls.close_poll(self.bot, pollid)
        await ctx.send(result)   
def setup(bot):
    bot.add_cog(PollCmds(bot))
