from constants import *
import os
import intentions


def main():
    servers_dir_name = config["servers_dir"]
    if os.path.isdir(servers_dir_name):
        os.makedirs(servers_dir_name)
    servers = config["servers"]
    for server in servers:
        server_name = server["name"]
        server_dir_name = os.path.join(servers_dir_name, server_name)
        if os.path.isdir(server_dir_name):
            os.makedirs(server_dir_name)

        # server_script = server["script"]
        # server_args = server["args"]

    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
