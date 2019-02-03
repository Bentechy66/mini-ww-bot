import discord
from discord.ext import commands

from wwbot.permissions import chk_gamemaster
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot.polls import create_poll, get_all_alive

class PollCmds():
    def __init__(self, bot):
        self.bot = bot

    @needs_game_phase(GamePhases.GAME)
    @chk_gamemaster
    @commands.group()
    async def poll(self, ctx):
        pass
    
    @poll.command()
    async def new(self, ctx):
        # creates a poll with options of all alive players for voting for everyone in this channel.
        await create_poll(ctx.channel, get_all_alive(self.bot))
    
    @poll.command()
    async def close(self, ctx, pollid : int):
        # closes that poll, puts results somewhere
        pass

def setup(bot):
    bot.add_cog(PollCmds(bot))
