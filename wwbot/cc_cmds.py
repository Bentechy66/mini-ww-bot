import discord
from discord.ext import commands

from wwbot.config import conf
from wwbot import ccs
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot.permissions import chk_participant

class CCCommands:
    # Cog class
    def __init__(self, bot):
        self.bot = bot

    @needs_game_phase(GamePhases.GAME)
    @chk_participant()
    @commands.group(invoke_without_command=True)
    async def cc(self, ctx):
        # nothing
        await ctx.send("You need to use a subcommand, see the help.")
    
    @cc.command()
    async def create(self, ctx, name, *people: discord.Member):
        """Create a Conspiracy Channel

        Create a new conspiracy channel with as many people as you want.
        Usage: `{PREFIX}create channel-name @person1 @person2 @person3...`
        """
        #await ctx.send("creating cc {} with people {}".format(name, ", ".join(str(p) for p in people)))
        await ctx.message.delete()
        await ccs.create_cc(self.bot,name,ctx.author,list(people)+[ctx.author])
    
    @cc.command()
    async def create_hidden(self, ctx, name, *people: discord.Member):
        """Create a Hidden Conspiracy Channel

        Create a new hidden conspiracy channel with as many people as you want.
        This works the same as ]create, except the people in the CC don't get told
        who the creator of the CC is.
        Usage: `{PREFIX}create channel-name @person1 @person2 @person3...`
        """
        #await ctx.send("creating hidden cc {} with people {}".format(name, ", ".join(str(p) for p in people)))
        await ctx.message.delete()
        await ccs.create_cc(self.bot,name,ctx.author,list(people)+[ctx.author],True)

    @cc.command()
    async def add(self, ctx, *people: discord.Member):
        """Adds people to a conspiracy channel

        Adds any number of people to the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        Usage: `{PREFIX}add @person1 @person2 @person3...`
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
    
    @cc.command()
    async def remove(self, ctx, *people: discord.Member):
        """Removes people from a conspiracy channel

        Removes any number of people from the conspiracy channel it was sent in.
        This is only available to the owner of that conspiracy channel.
        The owner of a conspiracy channel cannot be removed from that channel.
        Usage: `{PREFIX}remove @person1 @person2 @person3...`
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

    @cc.command(name="list")
    async def _list(self, ctx):
        """Lists people in a conspiracy channel

        Lists all the people currently in the conspiracy channel it was sent in.
        Usage: `{PREFIX}list`
        """
        people = ccs.get_cc_people(ctx.channel)
        await ctx.send("\n".join(m.mention for m in people))

def setup(bot):
    # extension setup function
    bot.add_cog(CCCommands(bot))
