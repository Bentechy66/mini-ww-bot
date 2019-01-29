import discord
from discord.ext import commands

from wwbot.config import conf
from wwbot import ccs

class CCCommands:
    # Cog class
    def __global_check(self, ctx):
        if not isinstance(ctx.cog, self.__class__):
            return True # only applies to these commands
        return (discord.utils.get(ctx.author.roles, id=conf['ids'].getint('participant')) is not None)

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, name, *people: discord.Member):
        """Create a Conspiracy Channel

        Create a new conspiracy channel with as many people as you want.
        Usage: `]create channel-name @person1 @person2 @person3...`
        """
        await ctx.send("creating cc {} with people {}".format(name, ", ".join(str(p) for p in people)))
        await ccs.create_cc(self.bot,name,ctx.author,list(people)+[ctx.author])
    
    @commands.command()
    async def create_hidden(self, ctx, name, *people: discord.Member):
        """Create a Hidden Conspiracy Channel

        Create a new hidden conspiracy channel with as many people as you want.
        This works the same as ]create, except the people in the CC don't get told
        who the creator of the CC is.
        Usage: `]create channel-name @person1 @person2 @person3...`
        """
        await ctx.send("creating hidden cc {} with people {}".format(name, ", ".join(str(p) for p in people)))
        await ccs.create_cc(self.bot,name,ctx.author,list(people)+[ctx.author],True)
    
    @commands.command()
    async def add(self, ctx, *people: discord.Member):
        """Adds people to a conspiracy channel

        Adds any number of people to the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        Usage: `]add @person1 @person2 @person3...`
        """
        # not using ext.commands checks because that effects the help system
        ccs.check_cc_owner(ctx)
        added = await ccs.add_to_cc(ctx.channel, people)
        if len(added) == 0:
            msg = "I didn't need to add anyone!"
        elif len(added) == 1:
            msg = "Welcome {0.mention} to {1.mention}".format(added[0], ctx.channel)
        else:
            all_mentions = [a.mention for a in added]
            people = ", ".join(all_mentions[:-1]) + " and " + all_mentions[-1]
            msg = "Welcome {0} to {1.mention}".format(people, ctx.channel)
        await ctx.send(msg)
    
    @commands.command()
    async def remove(self, ctx, *people: discord.Member):
        """Removes people from a conspiracy channel

        Removes any number of people from the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        The owner of a conspiracy channel cannot be removed from that channel.
        Usage: `]remove @person1 @person2 @person3...`
        """
        #await ctx.send("(TODO) removing people {}".format(", ".join(str(p) for p in people)))
        ccs.check_cc_owner(ctx)
        removed = await ccs.remove_from_cc(ctx.channel, people)
        if len(removed) == 0:
            msg = "I didn't need to remove anyone!"
        elif len(removed) == 1:
            msg = "{0.mention} has been removed from {1.mention}".format(removed[0], ctx.channel)
        else:
            all_mentions = [a.mention for a in removed]
            people = ", ".join(all_mentions[:-1]) + " and " + all_mentions[-1]
            msg = "{0} have all been removed from {1.mention}".format(people, ctx.channel)
        await ctx.send(msg)
    
    @commands.command(name="list")
    async def _list(self, ctx):
        """Lists people in a conspiracy channel

        Lists all the people currently in the conspiracy channel it was sent in.
        Usage: `]list`
        """
        people = ccs.get_cc_people(ctx.channel)
        await ctx.send("\n".join(m.mention for m in people))

def setup(bot):
    # extension setup function
    bot.add_cog(CCCommands(bot))
