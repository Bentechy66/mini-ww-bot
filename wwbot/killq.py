# kill queue.
import asyncio

import discord
from discord.ext import commands

from wwbot.permissions import chk_gamemaster
from wwbot.game_phase import needs_game_phase, GamePhases
from wwbot.db import KillQEntry
from wwbot.util import fetch_guild
from wwbot.config import conf

class KillQCmds:
    def __init__(self, bot):
        self.bot = bot
    
    @needs_game_phase(GamePhases.GAME)
    @chk_gamemaster
    @commands.group()
    async def killq(self, ctx):
        """Kill Queue management commands

        These are all gamemaster-only.
        With no subcommand, this will list the current kill queue.
        """
        q = list(KillQEntry.select())
        if len(q) == 0:
            await ctx.send("The Kill Queue is currently empty.")
        else:
            msg = "\n".join("- <@{0.discord_id}>".format(p) for p in q)
            await ctx.send("Current Kill Queue:\n" + msg)
    
    @killq.command()
    async def add(self, ctx, *who: discord.Member):
        """Add players to the kill queue.

        They must all be participants.
        """
        guild = fetch_guild(self.bot)
        participant = guild.get_role(conf['ids'].getint("participant"))
        if any(not participant in m.roles for m in who):
            await ctx.send(":warning: One or more of those people are not participants!")
            return
        KillQEntry.insert_many([{"discord_id":p.id} for p in who]).execute()
        await ctx.send(":white_check_mark: {} people added to kill queue!".format(len(who)))
    
    @killq.command()
    async def clear(self, ctx):
        """Clear the Kill Queue without killing anyone."""
        KillQEntry.delete().execute()
        await ctx.send("The Kill Queue has been cleared.")

    @killq.command()
    async def killall(self, ctx):
        """Kill everyone in the current Kill Queue.

        Each person in the Kill Queue will have their participant role removed and the dead role added.
        The Kill Queue will then be cleared.
        """
        guild = fetch_guild(self.bot)
        participant = guild.get_role(conf['ids'].getint("participant"))
        dead = guild.get_role(conf['ids'].getint("dead"))
        to_kill = list(KillQEntry.select())
        if len(to_kill) == 0:
            await ctx.send(":warning: The Kill Queue is empty!")
            return
        
        def check(m):
            return m.author.id == ctx.author.id and m.content.lower() == "ok" and m.channel == ctx.channel

        await ctx.send("All the above people will be killed by this command. Please type 'ok' here to confirm. This will expire in 10 seconds.")

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("Timed out.")
        else:
            for e in to_kill:
                member = guild.get_member(e.discord_id)
                await member.remove_roles(participant)
                await member.add_roles(dead)
                await ctx.send("Killed <@{}>".format(e.discord_id))
            KillQEntry.delete().execute()
            await ctx.send("The Kill Queue has been cleared.")


def setup(bot):
    bot.add_cog(KillQCmds(bot))
