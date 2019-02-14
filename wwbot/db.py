# database, peewee models, other db related stuff.
from peewee import *

from wwbot.config import conf

db = SqliteDatabase(conf['database']['filename'])

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    # needs to store name and emoji
    discord_id      = IntegerField(unique=True) 
    emoji           = CharField(unique=True)   # don't worry about length, sqlite doesn't care anyway

class Poll(BaseModel):
    channel         = IntegerField()

class PollMessage(BaseModel):
    discord_id      = IntegerField(unique=True) # discord id of the message in question
    poll            = ForeignKeyField(Poll, backref="messages")

class KillQEntry(BaseModel):
    discord_id      = IntegerField(unique=True)

class CCCategory(BaseModel):
    discord_id      = IntegerField(unique=True)

def create_tables():
    with db:
        print("Creating database tables in {}...".format(conf['database']['filename']))
        db.create_tables([Player, Poll, PollMessage, KillQEntry, CCCategory])
