import discord
from discord.ext import commands

from config import conf

class UserCommands:
    # Cog class
    def __global_check(self, ctx):
        if not isinstance(ctx.cog, self.__class__):
            return True # only applies to these commands
        return discord.utils.get(ctx.author.roles, id=self.participant_role_id)
        

    def __init__(self, participant_role_id):
        self.participant_role_id = participant_role_id

    @commands.command()
    async def create(self, ctx, name, *people):
        """Create a Conspiracy Channel

        Create a new conspiracy channel with as many people as you want.
        Usage: `]create channel-name @person1 @person2 @person3...`
        """
        await ctx.send("(TODO) creating cc {} with people {}".format(name, ", ".join(people)))


def setup(bot):
    # extension setup function
    bot.add_cog(UserCommands(conf['role_ids'].getint('participant')))
