import discord
from discord.ext import commands

from wwbot.util import fetch_guild, chunks
from wwbot.db import Player, Poll, PollMessage
from wwbot.permissions import is_participant
from wwbot import errors

def get_all_alive(bot):
    guild = fetch_guild(bot)
    alive = []
    for p in Player.select():
        m = guild.get_member(p.discord_id)
        if is_participant(m):
            alive.append(p)
    return alive

async def create_poll(ch, options):
    # options should have properties discord_id and emoji
    poll = Poll.create(channel=ch.id)
    await ch.send("Poll #`{}`".format(poll.id))
    msgids = []
    for chunk in chunks(options, 20):
        # chunk is a list of 20 Players from db
        pollmsg = await ch.send("\n".join("{0.emoji} - <@{0.discord_id}>".format(opt) for opt in chunk))
        msgids.append({"discord_id":pollmsg.id,"poll":poll})
        for p in chunk:
            await pollmsg.add_reaction(p.emoji)
    PollMessage.insert_many(msgids).execute()

async def get_raw_reactions(bot, poll, me):
    # returns a dict of emoji to members, with self removed
    # deletes reactions as they are collected
    reactions = {}
    channel = bot.get_channel(poll.channel)
    for dbmsg in poll.messages:
        msg = await channel.get_message(dbmsg.discord_id)
        for reaction in msg.reactions:
            users = await reaction.users().flatten()
            users.remove(me)
            reactions[reaction.emoji] = users
        await msg.clear_reactions()
    return reactions

async def process_reactions(reactions):
    # currently this just checks that no one has voted twice.
    # returns a dict of processed reactions and a list of error messages
    errs = []
    double_voted = set()
    all_users = set() # set of user ids
    for emoji, users in reactions.items():
        for user in users:
            if user.id in all_users:
                double_voted.add(user)
        all_users.update(set(u.id for u in users))
    for dv in double_voted:
        errs.append("{} has voted more than once! They have been disqualified.".format(dv.mention))
        for emoji, users in reactions.items():
            users.remove(dv)
    return reactions, errs

async def format_poll_output(bot, reactions, errs):
    guild = fetch_guild(bot)
    res_ret = []
    for emoji, people in reactions.items():
        option_player_id = Player.get(emoji=emoji).discord_id
        option_player_mention = guild.get_member(option_player_id).mention
        if len(people) == 0:
            voters = "*No one!*"
        else:
            voters = ", ".join(p.mention for p in people)
        res_ret.append(
            "({count}) {opt} : {voters}".format(
                opt=option_player_mention, voters=voters, count=len(people)
            )
        )
    return ("Results:\n" +
        "\n".join(res_ret) +
        "\n" +
        "\n".join(errs))


async def close_poll(bot, pollid):
    guild = fetch_guild(bot)
    poll = Poll.get_or_none(id=pollid)
    if poll is None:
        raise errors.NoSuchPoll()
    
    # get emojis to members, with self removed
    reactions = await get_raw_reactions(bot, poll, guild.me)

    # process the reactions
    processed_reactions, errs = await process_reactions(reactions)

    # format output
    s = await format_poll_output(bot, processed_reactions, errs)

    # delete the poll
    poll.delete_instance(recursive=True)
    return s
