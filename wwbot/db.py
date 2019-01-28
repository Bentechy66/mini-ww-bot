# database, peewee models, other db related stuff.
from peewee import *

from wwbot.config import conf

db = SqliteDatabase(conf['database']['filename'])

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    # needs to store name and emoji
    discord_id      = CharField(unique=True) # don't worry about length, sqlite doesn't care anyway
    emoji           = CharField(unique=True)

def create_tables():
    with db:
        print("Creating database tables in {}...".format(conf['database']['filename']))
        db.create_tables([Player])
