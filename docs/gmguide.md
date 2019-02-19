# Game Master Usage Guide
This guide will be a step-by-step process for running a game using the bot. If you're a player and
you want to use the bot, read [this guide](userguide.md) instead.

## Game Phases
A core system of the way this bot works is the concept of *Game Phases*. A Game Phase is a global
integer that describes what the overall current status of the system is. Currently, the game phases
supported by the bot are as follows:

| Id | Name | Description | Signups Open? | CCs and polls available |
|----|------|-------------|---------------|-------------------------|
|0|`NOTHING`|The bot does not really do anything|*No*|*No*|
|1|`SIGNUP`|Signups are open, game not in progress|**Yes**|*No*|
|2|`GAME`|Game in progress|*No*|**Yes**|

When the bot is switched on for the first time it will be in Game Phase `NOTHING` (0). The current
game phase is saved when the bot is shut down and loaded when it is started again.

### Game Phase commands
The command `{PREFIX}gamephase` can be used by Game Masters to query the current game phase. Game
Masters can also use `{PREFIX}gamephase set <id_or_name>` to change the current game phase.

### Example Game Phase Usage
- Initially: `NOTHING` (0).
- Open up signups: `SIGNUP` (1).
- Close signups after reaching the required number of players: `NOTHING` (0)
- Decide on roles, send them out to players.
- Open the actual game: `GAME` (2).

### `start_game` command
The `{PREFIX}start_game` command is a convienience command that assigns the Participant role
to all signed-up people, then switches to game phase `GAME` (2).

## Polls
Polls can be created in the current channel with the command `{PREFIX}poll new`. The options on
polls will be all currently alive players. The ID number for the poll will also be printed out.

To close a poll, use `{PREFIX}poll close <id>`. This will count (and then clear) all reactions from
the given poll, then print out the results into the channel the close command was sent from. If you
want the raw results of the poll to be kept private for whatever reason, run the close command in a
private channel.

Please note that the bot doesn't attempt to calculate the winner of a poll, because many people will
have special voting rules (like the mayor's double vote, or demonised players' votes not counting, etc).

## Killing
Killing players is managed through a system called the *Kill Queue*. The Kill Queue contains a list
of all the players who will be killed when the queue is executed.

To list the current contents of the kill queue, use `{PREFIX}killq`. To add players to the kill queue,
use `{PREFIX}killq add <@player1> [<@player2> [... ]]`. To kill all the players on the kill queue, use
`{PREFIX}killq killall`. To clear the kill queue without killing anyone, use `{PREFIX}killq clear`.
