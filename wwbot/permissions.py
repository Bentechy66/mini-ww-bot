# general stuff for permission management
from wwbot.config import conf
from wwbot import errors
import discord
from discord.ext import commands

participant = conf['ids'].getint("participant")
gamemaster  = conf['ids'].getint("gamemaster")

def is_participant(member):
    p_role = discord.utils.get(member.roles, id=participant)
    return p_role is not None

def is_gamemaster(member):
    gm_role = discord.utils.get(member.roles, id=gamemaster)
    return gm_role is not None

@commands.check
def chk_participant(ctx):
    if is_participant(ctx.author):
        return True
    else:
        raise errors.NeedsParticipant()

@commands.check
def chk_gamemaster(ctx):
    if is_gamemaster(ctx.author):
        return True
    else:
        raise errors.NeedsGM()

