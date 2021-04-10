from global_modules import *
import intentions


def test_main(argv):
    discord_client.run(configs.current_config["bot_token"])
