import discord
from discord.ext import commands

from config import conf
import ccs

class UserCommands:
    # Cog class
    def __global_check(self, ctx):
        if not isinstance(ctx.cog, self.__class__):
            return True # only applies to these commands
        return discord.utils.get(ctx.author.roles, id=conf['ids'].getint('participant'))

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, name, *people: discord.Member):
        """Create a Conspiracy Channel

        Create a new conspiracy channel with as many people as you want.
        Usage: `]create channel-name @person1 @person2 @person3...`
        """
        await ctx.send("creating cc {} with people {}".format(name, ", ".join([str(p) for p in people])))
        await ccs.create_cc(self.bot,name,ctx.author,list(people)+[ctx.author])
    
    @commands.command()
    async def add(self, ctx, *people):
        """Adds people to a conspiracy channel

        Adds any number of people to the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        Usage: `]add @person1 @person2 @person3...`
        """
        await ctx.send("(TODO) adding people {}".format(", ".join(people)))
    
    @commands.command()
    async def remove(self, ctx, *people):
        """Removes people from a conspiracy channel

        Removes any number of people from the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        The owner of a conspiracy channel cannot be removed from that channel.
        Usage: `]remove @person1 @person2 @person3...`
        """
        await ctx.send("(TODO) removing people {}".format(", ".join(people)))
    
    @commands.command(name="list")
    async def _list(self, ctx, *people):
        """Lists people in a conspiracy channel

        Lists all the people currently in the conspiracy channel it was sent in.
        Usage: `]list`
        """
        await ctx.send("(TODO) listing"

    @commands.command()
    async def owner(self, ctx):
        await ctx.send(str(ccs.get_cc_owner(ctx.channel)))

def setup(bot):
    # extension setup function
    bot.add_cog(UserCommands(bot))
