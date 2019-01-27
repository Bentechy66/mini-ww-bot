from configparser import ConfigParser
import logging
logger = logging.getLogger(__name__)
import sys
import os

conf = ConfigParser()

conffile = os.getenv("CCBOT_CONFIGFILE","config.ini")

try:
    with open(conffile) as f:
        conf.read_file(f)
except FileNotFoundError:
    logger.critical("File not found: {} - ensure it is in your current directory or update envvar CCBOT_CONFIGFILE".format(conffile))
    sys.exit(1)
