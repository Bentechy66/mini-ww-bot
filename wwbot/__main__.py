import os
import sys
import traceback

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s::%(name)s@%(asctime)s : %(message)s')
logger = logging.getLogger("wwbot")

from wwbot.errors import WWBotException

import discord
from discord.ext import commands

bot = commands.Bot("]")

token = os.getenv("WWBOT_TOKEN",None)
if token is None:
    sys.exit("Please set envvar WWBOT_TOKEN to your bot's token")


@bot.event
async def on_ready():
    logger.info("Logged in!")

extensions = (
    "cc_cmds",
    "signup",
    "poll_cmds",
    "killq",
    "game_phase_cmds",
)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@commands.is_owner()
@bot.command()
async def stop(ctx):
    raise SystemExit()

@bot.command()
async def temp_set_gp(ctx, new: int):
    from wwbot.game_phase import set_game_phase
    set_game_phase(new)

for ext in extensions:
    bot.load_extension("wwbot."+ext)

# errors
@bot.event
async def on_command_error(ctx, error):
    # todo: nicer error handling for certain errors
    if isinstance(error, (WWBotException, commands.CommandError)):
        await ctx.send(":warning: "+str(error))
    else:
        errstr = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        logger.error("Error in command {}:\n{}".format(ctx.command, errstr))
        await ctx.send("An error occured: {} - {}\nPlease see console for details.".format(error.__class__.__name__, str(error)))

if __name__ == "__main__":
    bot.run(token)
