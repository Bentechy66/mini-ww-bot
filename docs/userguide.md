# WW Bot User Guide
This is intended for people who are players on a server that uses this bot. If you're a GM
and you want to run a game, use [this guide](gmguide.md) instead.

### Notations
In this guide, the notation `{PREFIX}command` will be used for commands, where `{PREFIX}`
should be replaced with whatever the command prefix for the server is. So if the server prefix
is `.` and the documentation said `{PREFIX}cc create` then you would write `.cc create`.

In command descriptions, `<>` is used for parameters that you should fill in. `[]` is used for
optional paramaters and `...` means you can add as many more parameters as you want. Remember
not to include these when you actually run the command!

# Refering to people
Many different commands this bot uses can take people as an argument to that command. You can
specify people to commands in any of the following ways:
- As a mention. This is probably the simplest way. Just ping them like you would normally.
- As a username. This is useful if, for example, you want to add someone to a CC and can't ping
them because they're not in that CC. Please note that if their username has a space in it you 
need to put it in quotes, like this: `{PREFIX}cc add "Person With A Long Name"`

Currently, you can't use someone's emoji to refer to them. This feature is Coming Soon&trade;,
however.

# CCs
Probably the most important thing you will use this bot for is managing CCs. The `{PREFIX}cc`
command is used for creating and managing CCs.

## Creating CCs
To create a CC, use the `{PREFIX}cc create <name> <person> [ <person> [ ... ] ]`. `<name>` is the
name of the CC you want to create: don't forget to include it. `<person>` are the people you want
to add.

Example: to create a CC called "secret" with @person1 and @person2 in it, you would use this command:
`{PREFIX}cc create secret @person1 @person2`.

Your message with this command in will be deleted so no one else knows you created the CC.

## Hidden CCs
The `{PREFIX}cc create_hidden` command can be used to create hidden CCs. A hidden CC is like a
normal CC, but the bot does not announce the who the creator is, meaning no one knows who made the
CC (unless you tell them).

The command is used in exactly the same way as the `{PREFIX}cc create` command.

## Adding and Removing People
You can only add people to or remove people from a CC if you are the person who created that CC.
Use the `{PREFIX}cc add <person> [ <person> [ ... ] ]` command to add people and the
`{PREFIX}cc remove <person> [ <person> [ ... ] ]` command to remove people from the CC you
typed the command in.

Example: to remove @person1 from a CC, you would type `{PREFIX}cc remove @person1` *in that CC*.

## Listing people
You probably won't need this, but you can type `{PREFIX}cc list` in any CC to list the people in that
CC.

# Miscellanious other commands
## Signing up
To sign up for a game do this: `{PREFIX}signup <emoji>`. For instance to sign up with the emoji
🗑, do `{PREFIX}signup 🗑`.

## Listing players
To list every player in the current game along with their emoji, whether they are alive or not, use
`{PREFIX}list_signedup`.

## Random other stuff you can do
`{PREFIX}gamephase` will tell you what the bot's current internal Game Phase is. This is probably
only interesting if you're a Game Master.

`{PREFIX}ping` will make the bot say "pong". This is for testing if the bot is alive. Please don't
spam it.
