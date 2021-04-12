from constants import *
import constants
import mc
import os


def main():
    servers_dir_name = config["servers_dir"]
    if not os.path.isdir(servers_dir_name):
        os.makedirs(servers_dir_name)

    server_json_objs = config["servers"]
    for server_json_obj in server_json_objs:
        server_name = server_json_obj["name"]
        server_dir_name = os.path.join(servers_dir_name, server_name)
        if not os.path.isdir(server_dir_name):
            os.makedirs(server_dir_name)

        server_obj = mc.Server(
            server_json_obj["name"], server_json_obj["script"], config, logger)

        constants.servers.append(server_obj)

    import intentions #to register all intentions
    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
