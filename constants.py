from typing import List

import common
import db
import dc
import mc

# initialization of Database
database = db.Database("data.db")
# initialization of Tables
database.init_table(
    "admins",
    {
        "user_id": str,
    }
)

# initialize common objects
config = common.Config()
logger = common.Logger()
bot = dc.Bot(config, logger)

servers: List[mc.Server] = []
