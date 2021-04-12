from typing import List
import common
import dc
import mc

config = common.Config()
logger = common.Logger()
bot = dc.Bot(config, logger)

servers: List[mc.Server] = []
