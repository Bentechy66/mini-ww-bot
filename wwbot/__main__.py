import os
import sys
import traceback

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s::%(name)s@%(asctime)s : %(message)s')
logger = logging.getLogger("wwbot")

from wwbot.errors import WWBotException

import discord
from discord.ext import commands

from wwbot.config import conf

prefix = conf['general']['prefix']
bot = commands.Bot(prefix)

token = os.getenv("WWBOT_TOKEN",None)
if token is None:
    sys.exit("Please set envvar WWBOT_TOKEN to your bot's token")


extensions = (
    "cc_cmds",
    "signup",
    "poll_cmds",
    "killq",
    "game_phase_cmds",
    "roles",
)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.event
async def on_ready():
    logger.info("Logged in, loading extensions...")
    for ext in extensions:
        bot.load_extension("wwbot."+ext)
    logger.info("{} extensions loaded. Done!".format(len(extensions)))


@bot.command()
async def _t_rm(ctx, r="Innocent"):
    await ctx.send(conf['general']['role_message'].format(role=r))
# errors
@bot.event
async def on_command_error(ctx, error):
    # todo: nicer error handling for certain errors
    if isinstance(error, (WWBotException,)):
        await ctx.send(":warning: "+str(error))
    else:
        errstr = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        logger.error("Error in command {}:\n{}".format(ctx.command, errstr))
        await ctx.send(":warning: An error occured: {} (`{}`)".format(str(error), error.__class__.__name__))

if __name__ == "__main__":
    bot.run(token)
