# script for doing database management, mainly
import sys
from wwbot.db import create_tables
from wwbot.config import conf

def m_role_column():
    "add the role column to player table"
    from playhouse.migrate import migrate, SqliteMigrator
    from peewee import CharField
    from wwbot.db import db
    db.connect()
    field = CharField(default="")
    migrator = SqliteMigrator(db)
    migrate(
        migrator.add_column('player', 'role', field)
    )

def main():
    if len(sys.argv) != 2:
        sys.exit("Please specify the command you want me to run.")
        
    if sys.argv[1] == "create_tables":
        print("Creating db tables")
        create_tables()
        print("All done!")

    elif sys.argv[1] == "m_role_column":
        print("migration - adding role column to Player table")
        m_role_column()
        print("All Done!")
    
    else:
        sys.exit("I don't know what you want me to do!")

if __name__ == "__main__":
    main()
