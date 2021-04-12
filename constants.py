from typing import List
import common
import dc
import mc
import db
import admins

database = db.Database("data.db")
admins_table = admins.create_table(database)
admins_table.create()

config = common.Config()
logger = common.Logger()
bot = dc.Bot(config, logger)

servers: List[mc.Server] = []
