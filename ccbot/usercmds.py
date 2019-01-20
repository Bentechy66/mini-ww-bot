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
    
    @commands.command()
    async def add(self, ctx, *people):
        """Adds people to a conspiracy channel

        Adds any number of people to the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        Usage: `]add @person1 @person2 @person3...`
        """
        await ctx.send("(TODO) adding people {}".format(name, ", ".join(people)))
    
    @commands.command()
    async def remove(self, ctx, *people):
        """Removes people from a conspiracy channel

        Removes any number of people from the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        The owner of a conspiracy channel cannot be removed from that channel.
        Usage: `]remove @person1 @person2 @person3...`
        """
        await ctx.send("(TODO) removing people {}".format(name, ", ".join(people)))
    
    @commands.command(name="list")
    async def _list(self, ctx, *people):
        """Lists people in a conspiracy channel

        Lists all the people currently in the conspiracy channel it was sent in.
        If the conspiracy channel is not a hidden channel then the owner will
        be listed as well.
        Usage: `]list`
        """
        await ctx.send("(TODO) listing".format(name, ", ".join(people)))


def setup(bot):
    # extension setup function
    bot.add_cog(UserCommands(conf['role_ids'].getint('participant')))
