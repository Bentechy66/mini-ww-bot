# Mini-WW-Bot
Very simple bot to automate the boring stuff in a werewolves server
## Setup
Do a git clone to get the source.

To install the dependencies do `pip install -r requirements.txt`.

You will then want to set up the bot. Edit the config file as described below.

To initialise the database, run `python3 housekeeping.py create_tables`

To run the bot, the envvar `WWBOT_TOKEN` must be set to your discord bot token. This is required and the bot will fail if you don't do this.

Once you've set everything up correctly, you can then run the bot with `python3 -m wwbot` from the root dir.

### The config file
By default, this will look for a file called `config.ini` in your current working directory. If you want to change this, set the envvar `WWBOT_CONFIGFILE` to the path to your config file.

Values in the file to configure various discord ids are all in the section `[ids]`, and are as follows:
- `guild`: the id of the guild you are running the bot in
- `category`: the id of the category to put CCs in
- `participant`: the id of the participant role (people who are allowed to create CCs)

Values in this file to configure the database are in the section `[database]`, and are as follows:
- `filename`: the filename, relative to the current working dir, of the SQLite database to use.
- `gamephase_filename`: the filename, relative to the current working dir, of the game state file to use. Currently this file will just contain an integer that represents the global phase of the game (see the comment at the top of `wwbot/game_phase.py` for an explaination). This file gets loaded on startup and saved on exit.

You can also configure the bot command prefix: this is in the section `[general]`, with the key name `prefix`. This is currently the only key in the `[general]` section.

## Usage
See the [GM Guide](https://ed588.github.io/mini-ww-bot/gmguide.html) for Game Master usage information.
