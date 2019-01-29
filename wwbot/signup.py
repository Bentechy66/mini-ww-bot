import discord
from discord.ext import commands

from wwbot import errors
from wwbot.util import is_emoji_str

from wwbot.db import db, Player

def signup_or_change(member, emoji):
    # returns bool (worked or not) and str (message to print)
    # first check if someone is already using that emoji
    p = Player.get_or_none(Player.emoji == emoji)
    if p is not None:
        if p.discord_id == str(member.id):
            msg = "You are"
        else:
            msg = "Someone else is"
        return False, msg+" already using the emoji {}!".format(emoji)

    p = None
    p = Player.get_or_none(Player.discord_id == member.id)
    if p is None:
        # create the player and add it
        Player.create(discord_id=member.id, emoji=emoji)
        return True, "{} signed up with emoji {}".format(member.mention, emoji)
    else:
        # update the player
        p.emoji = emoji
        p.save()
        # well that was easy
        return True, "{} changed their emoji to {}.".format(member.mention, emoji)


class SignupCmds:
    @commands.command()
    async def signup(self, ctx, emoji):
        if not is_emoji_str(emoji):
            await ctx.send("{} is not an emoji!".format(emoji))
            return
        worked, msg = signup_or_change(ctx.author, emoji)
        if worked:
            status = ":white_check_mark: "
        else:
            status = ":warning: "
            
        await ctx.send(status + msg)
    
    @commands.command()
    async def list_signedup(self, ctx):
        await ctx.send("\n".join("{} - <@{}>".format(p.emoji, p.discord_id) for p in Player.select()))

def setup(bot):
    bot.add_cog(SignupCmds())
