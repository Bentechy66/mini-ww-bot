import discord
from discord.ext import commands

from wwbot import errors
from wwbot.util import is_emoji_str, fetch_guild
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot.db import db, Player
from wwbot.permissions import chk_gamemaster

def signup_or_change(member, emoji):
    # returns bool (new or not) and str (message to print)
    # first check if someone is already using that emoji
    p = Player.get_or_none(Player.emoji == emoji)
    if p is not None:
        msg = ":warning: "
        if p.discord_id == member.id:
            msg += "You are"
        else:
            msg += "Someone else is"
        return msg+" already using the emoji {}!".format(emoji)

    p = None
    p = Player.get_or_none(Player.discord_id == member.id)
    if p is None:
        # create the player and add it
        Player.create(discord_id=member.id, emoji=emoji)
        return ":white_check_mark: {} signed up with emoji {}".format(member.mention, emoji)
    else:
        # update the player
        p.emoji = emoji
        p.save()
        # well that was easy
        return ":white_check_mark: {} changed their emoji to {}.".format(member.mention, emoji)

async def remove_player(member):
    p = Player.get_or_none(Player.discord_id == member.id)
    if p == None:
        return False
    p.delete_instance()
    return True

class SignupCmds:
    def __init__(self, bot):
        self.bot=bot

    @needs_game_phase(GamePhases.SIGNUP)
    @commands.command()
    async def signup(self, ctx, emoji):
        if not is_emoji_str(emoji):
            await ctx.send("{} is not an emoji!".format(emoji))
            return
        msg = signup_or_change(ctx.author, emoji)
        await ctx.send(msg)
    
    @needs_game_phase(GamePhases.SIGNUP)
    @chk_gamemaster()
    @commands.command()
    async def unsignup(self, ctx, who: discord.Member):
        worked = await remove_player(who)
        if worked:
            await ctx.send(":white_check_mark: Player {} is no longer signed up".format(who))
        else:
            await ctx.send("That person wasn't signed up anyway so I didn't do anything.")

    @commands.command()
    async def list_signedup(self, ctx):
        guild = fetch_guild(self.bot)
        players = list(Player.select())
        count = len(players)
        if count == 0:
            await ctx.send("No one has signed up yet!")
        else:
            await ctx.send(
                "*Total: {} players*\n".format(count) + 
                "\n".join(
                    "{} - {}".format(p.emoji, guild.get_member(p.discord_id).display_name) for p in players
                ))

def setup(bot):
    bot.add_cog(SignupCmds(bot))
