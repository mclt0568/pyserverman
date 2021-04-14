from constants import *
import constants
import mc
import os

def main():
    servers_dir_name = config["servers_dir"]
    if not os.path.isdir(servers_dir_name):
        os.makedirs(servers_dir_name)

    import intentions
    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
