from time import sleep
from io import BytesIO
from json import load

import discord
from discord.ext import commands

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
        await ctx.send("⚠️ You didn't specify a subcommand!")

        
    @readme.command()
    async def push(self, ctx, channel_id: int = 0, msg_send_interval: int = 0):
        # Let's create a series of #readme-capable embeds. If something is uploaded,
        # It will attempt to use that file for the readme, if omitted, it will use
        # the default JSONifed readme file and send that into the channel instead.

        # The user has uploaded a config.
        if ctx.message.attachments != []:
            message_attachment = ctx.message.attachments[0]

            json_config = load(BytesIO(message_attachment.save()))

            await ctx.send(":white_check_mark: Creating README using uploaded config file")

        # No config uploaded, just use default config file.
        else:
            with open("readme.json", "rb") as default_json:
                json_config = load(default_json)

            await ctx.send(":ballot_box_with_check: Creating README using default config file.")

        for section in json_config:
            # Initialise our message and embed variables each loop.
            # This is to prevent leftover data from being re-sent.
            msg_content, current_embed = None, None

            # The part which handles general messages.
            if "content" in json_config[section]:
                msg_content = json_config[section]["content"]

            # We have an embed. Call in the Seahawks.
            if "embed" in json_config[section]:
                current_embed = discord.Embed()
                msg_embed = json_config[section]["embed"]
                if "text" in msg_embed:
                    current_embed.description = msg_embed["text"]
                if "color" in msg_embed:
                    current_embed.colour = discord.Colour(int(msg_embed["color"], 16))

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
                file=discord.File(raw_json, 'readme.json')
            )
            await ctx.send(":airplane: **Flying in, check your DMs!**")

def setup(bot):
    bot.add_cog(ReadmeCommands(bot))
