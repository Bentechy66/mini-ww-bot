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

def chk_participant():
    def predicate(ctx):
        if is_participant(ctx.author):
            return True
        else:
            raise errors.NeedsParticipant()
    return commands.check(predicate)

def chk_gamemaster():
    def predicate(ctx):
        if is_gamemaster(ctx.author):
            return True
        else:
            raise errors.NeedsGM()
    return commands.check(predicate)

def is_gm_channel(channel):
    topic = channel.topic
    if topic is None:
        return False
    elif "GMSAFE" in topic:
        return True
    else:
        return False

def chk_gm_channel():
    def predicate(ctx):
        if is_gm_channel(ctx.channel):
            return True
        else:
            raise errors.NeedsGmChannel()
    return commands.check(predicate)
