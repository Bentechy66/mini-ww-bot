import discord
from discord.ext import commands

from wwbot.permissions import chk_gamemaster
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot import polls

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
        await polls.create_poll(ctx.channel, polls.get_all_alive(self.bot))
    
    @poll.command()
    async def close(self, ctx, pollid : int):
        # closes that poll, puts results somewhere
        reactions = await polls.close_poll(self.bot, pollid)
        await ctx.send("Results for poll #`{}`:".format(pollid))
        for emoji, people in reactions.items():
            await ctx.send("{} - {} ({})".format(emoji, len(people), ", ".join(str(p) for p in people)))
def setup(bot):
    bot.add_cog(PollCmds(bot))
