import json
import os
import threading
from typing import Any


class Config:
    def __init__(self, filename: str) -> None:
        self.config = {
            "bot": {
                "token": "",
                "guild": 0,
                "channel": 0
            },
            "servers_dir": "servers",
            "servers": [
                {
                    "name": "",
                    "script": "",
                }
            ]
        }
        self.config_filename = filename

        self.config_file_lock = threading.Lock()
        if not os.path.isfile(self.config_filename):
            open(self.config_filename, "w", encoding="utf8").close()
            self.save_config()
        else:
            self.sync_config()

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def sync_config(self) -> None:
        with self.config_file_lock:
            with open(self.config_filename, "r", encoding="utf8") as config_file:
                self.config = json.load(config_file)

    def save_config(self) -> None:
        with self.config_file_lock:
            with open(self.config_filename, "w", encoding="utf8") as config_file:
                json.dump(self.config, config_file, indent=4)
