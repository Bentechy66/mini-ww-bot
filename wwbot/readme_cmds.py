from time import sleep
from io import StringIO
from json import load

import discord
from discord import Colour, Embed, File, Message
from discord.ext import commands
from aiohttp import ClientSession

from wwbot.config import conf
from wwbot.permissions import chk_gamemaster
    
    
class ReadmeCommands(commands.Cog, name="Readme"):
    def __init__(self, bot):
        self.bot = bot

    @chk_gamemaster()
    @commands.group(invoke_without_command=True)
    async def readme(self, ctx: commands.Context):
        """
        Allows generating, sending and manipulation of JSON file containing the info needed
        to create and send the embeds for the #readme channel. Only Game Masters have
        the permissions need to use this command.
        """
        incorrect_operand_embed = Embed(
            colour=0x673ab7,
            description=":shrug: **No subcommand specified.**"
        )
        await ctx.send(embed=incorrect_operand_embed)

        
    @readme.command()
    async def push(self, ctx, channel_id: int = 0, msg_send_interval: int = 0):
        # Let's create a series of #readme-capable embeds. If something is uploaded,
        # It will attempt to use that file for the readme, if omitted, it will use
        # the default JSONifed readme file and send that into the channel instead.
        usr_confirmation_embed = Embed(
            colour=0x4caf50,
            description=":white_check_mark: **Creating readme using uploaded config file.**"
        )

        # The user has uploaded a config.
        if ctx.message.attachments != []:
            json_file_location = [_.url for _ in ctx.message.attachments][0]

            # GETs the attachment data.
            async with ClientSession() as session:
                async with session.get(json_file_location) as response:
                    if response.status == 200:
                        resp_text = await response.text()

            json_config = load(StringIO(resp_text))
            await ctx.send(embed=usr_confirmation_embed)

        # No config uploaded, just use default config file.
        else:
            with open("readme.json", "rb") as default_json:
                json_config = load(default_json)

            usr_confirmation_embed.description = (":ballot_box_with_check: "
                                                    "**Creating readme using default config file.**")
            await ctx.send(embed=usr_confirmation_embed)

        for section in json_config:
            # Initialise our message and embed variables each loop.
            # This is to prevent leftover data from being re-sent.
            msg_content, current_embed = None, None

            # The part which handles general messages.
            if "content" in json_config[section]:
                msg_content = json_config[section]["content"]

            # We have an embed. Call in the Seahawks.
            if "embed" in json_config[section]:
                current_embed = Embed()
                msg_embed = json_config[section]["embed"]
                if "text" in msg_embed:
                    current_embed.description = msg_embed["text"]
                if "color" in msg_embed:
                    current_embed.colour = Colour(int(msg_embed["color"], 16))

                # Parse the fields, if there are any.
                if "fields" in msg_embed:
                    for current_field in msg_embed["fields"]:
                        # Add the fields to the current embed.
                        current_embed.add_field(
                            name=current_field["name"],
                            value=current_field["value"]
                        )

            # Send the message.
            requested_channel = self.bot.get_channel(channel_id)

            if (msg_content is not None and current_embed is None):
                await requested_channel.send(content=msg_content)
            elif (current_embed is not None and msg_content is None):
                await requested_channel.send(embed=current_embed)
            else:
                await requested_channel.send(content=msg_content, embed=current_embed)

            # User has requested a delay between each message being sent.
            if (0 < msg_send_interval < 901):
                await sleep(msg_send_interval)

    @readme.command()
    async def pull(self, ctx):
        # Get the human-readble readme data.
        with open("readme.json", "rb") as readme_json:
            raw_json = readme_json.read()

            # Slide it to the user's DMs.
            requesting_user = await self.bot.get_user_info(ctx.message.author.id)
            await requesting_user.send(
                content="Hey, here's your readme config file!",
                file=File(raw_json, 'readme.json')
            )

            msg_confirmation = Embed(
                colour=0x009688,
                description=":airplane: **Flying in, check your DMs!**"
            )
            await ctx.message.delete()
            await ctx.send(embed=msg_confirmation)

def setup(bot):
    bot.add_cog(ReadmeCommands(bot))
