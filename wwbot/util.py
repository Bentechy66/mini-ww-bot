# misc utility functions
import emoji

def is_emoji_str(s):
    # returns whether s is a string containing nothing but a single emoji
    er = emoji.get_emoji_regexp()
    return len(s) == 1 and er.match(s)
