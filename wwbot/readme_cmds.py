import discord
from discord.ext import commands, has_role, command

from wwbot.config import conf
    
    
class ReadmeCommands(commands.cog, name="Readme"):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @has_role(conf["ids"]["gamemaster"])
    async def readme(self, ctx: Context, operand: str = "", channel_id: int = 0, msg_send_interval: int = 0):
        """
        Allows generating, sending and manipulation of JSON file containing the info needed
        to create and send the embeds for the #readme channel. Only Game Masters have
        the permissions need to use this command.
        """

        README_SEND_ALIASES = ["create", "push", "generate", "send", "make", "build", "upload"]
        README_RECV_ALIASES = ["fetch", "get", "pull", "download", "retrieve", "dm", "dl"]

        operand = operand.lower()

        # The supplied operand is incorrect.
        if not (operand in README_SEND_ALIASES + README_RECV_ALIASES):
            incorrect_operand_embed = Embed(
                colour=0x673ab7,
                description=":shrug: **Invalid readme operand supplied.**"
            )
            await ctx.message.delete()
            await ctx.send(embed=incorrect_operand_embed)

        # User missed out the channel_id for certain commands.
        elif (channel_id == 0 and operand in README_SEND_ALIASES):
            misssing_channel_embed = Embed(
                colour=0xff5722,
                description=":facepalm: **Whoops, you missed out the channel ID! Try again.**"
            )
            await ctx.message.delete()
            await ctx.send(embed=misssing_channel_embed)

        # Process the request.
        else:
            # Let's create a series of #readme-capable embeds. If something is uploaded,
            # It will attempt to use that file for the readme, if omitted, it will use
            # the default JSONifed readme file and send that into the channel instead.
            if operand in README_SEND_ALIASES:
                try:
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

                    await ctx.message.delete()

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

                except(Exception):
                    parse_fail_embed = Embed(
                        colour=0x673ab7,
                        description=":x: **Error parsing JSON file, please ensure its valid!**"
                    )
                    await ctx.message.delete()
                    await ctx.send(embed=parse_fail_embed)

            # Pull the readme JSON constant files and slide it into the user's DMs.
            elif operand in README_RECV_ALIASES:
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
