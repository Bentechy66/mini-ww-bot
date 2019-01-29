import discord
from discord.ext import commands

from wwbot import signup
from wwbot.db import db, Player

def signup_or_change(member, emoji):
    # returns whether the player already existed
    p = Player.get_or_none(Player.discord_id == member.id)
    if p is None:
        # create the player and add it
        Player.create(discord_id=member.id, emoji=emoji)
        return False
    else:
        # update the player
        p.emoji = emoji
        p.save()
        # well that was easy
        return True


class SignupCmds:
    @commands.command()
    async def signup(self, ctx, emoji: discord.Emoji):
        already = signup.signup_or_change(ctx.author, emoji)
        if already:
            await ctx.send(":white_check_mark: {} changed their emoji to {}.".format(ctx.author.mention, emoji))
        else:
            await ctx.send(":white_check_mark: {} signed up with emoji {}".format(ctx.author.mention, emoji))
    
    @commands.command()
    async def list_signedup(self, ctx):
        await ctx.send("\n".join("{} - <@{}>".format(p.emoji, p.discord_id) for p in Player.select()))

def setup(bot):
    bot.add_cog(SignupCmds())
