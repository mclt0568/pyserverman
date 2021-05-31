import os

from constants import *


def main():
    servers_dir_name = config["servers_dir"]
    if not os.path.isdir(servers_dir_name):
        os.makedirs(servers_dir_name)

    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
