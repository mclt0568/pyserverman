from global_modules import *


def test_main(argv):
    discord_client.run(configs.current_config["bot_token"])
