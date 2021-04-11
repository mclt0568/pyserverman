from constants import *
import os
import mc
import intentions


def main():
    servers_dir_name = config["servers_dir"]
    if not os.path.isdir(servers_dir_name):
        os.makedirs(servers_dir_name)
    servers = config["servers"]
    server_objs = []
    for server in servers:
        server_name = server["name"]
        server_dir_name = os.path.join(servers_dir_name, server_name)
        if not os.path.isdir(server_dir_name):
            os.makedirs(server_dir_name)

        server_objs.append(mc.Server(server["script"]))
    
    for server_obj in server_objs:
        server_obj.run()

    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
