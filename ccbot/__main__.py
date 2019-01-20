import os
import sys

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s::%(name)s@%(asctime)s : %(message)s')
logger = logging.getLogger("ccbot")

import discord
from discord.ext import commands

bot = commands.Bot("]")

token = os.getenv("CCBOT_TOKEN",None)
if token is None:
    sys.exit("Please set envvar CCBOT_TOKEN to your bot's token")

from config import conf
print(conf['role_ids']['admin'])

@bot.event
async def on_ready():
    logger.info("Logged in!")

extensions = (
    "usercmds",
)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

for ext in extensions:
    bot.load_extension(ext)

# errors
#@bot.event
async def on_command_error(ctx, error):
    # todo: nicer error handling for certain errors
    await ctx.send("An error occurred: "+str(error))

bot.run(token)
