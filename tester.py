from global_modules import *
import intentions


def test_main(argv):
    discord_client.run(config["bot"]["token"])
