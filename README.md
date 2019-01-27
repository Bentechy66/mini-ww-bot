# CC Bot
Very simple bot to create CCs in a werewolves server
## How to use
Do a git clone to get the source.

To install the dependencies do `pip install -r requirements.txt`.

The envvar `CCBOT_TOKEN` must be set to your discord bot token. This is required and 
the bot will fail if you don't do this.

You can then run the bot with `python3 ccbot` from the root dir.

### The config file
By default, this will look for a file called `config.ini` in your current working directory. If you want to change this, set the envvar `CCBOT_CONFIGFILE` to the path to your config file.

Currently the only values in the file are all in the section `[ids]`, and are as follows:
- `guild`: the id of the guild you are running the bot in
- `category`: the id of the category to put CCs in
- `participant`: the id of the participant role (people who are allowed to create CCs)
