# script for doing database management, mainly
import sys
from wwbot.db import create_tables
from wwbot.config import conf

def main():
    if len(sys.argv) != 2:
        sys.exit("Please specify the command you want me to run.")
        
    if sys.argv[1] == "create_tables":
        print("Creating db tables")
        create_tables()
        print("All done!")
    
    else:
        sys.exit("I don't know what you want me to do!")

if __name__ == "__main__":
    main()
