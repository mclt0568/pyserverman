from typing import Any, Dict, IO
from exceptions import ConfigError
import json
import os
import threading


class Config:
    config: Dict[str, Any]
    config_filename: str
    config_template: Dict[str, Any]

    config_file: IO
    config_file_lock: threading.Lock

    def __init__(self) -> None:
        self.config_filename = "config.json"

        self.config_template = {
            "bot_token": "",
            "server_script": "",
            "server_args": [],
            "default_server_guild": 0,
            "default_server_channel": 0,
            "default_admins": []
        }

        if not os.path.isfile(self.config_filename):
            self.config_file = open(self.config_filename, "w+")
            json.dump(self.config_template, self.config_file, indent=2)
        else:
            self.config_file = open(self.config_filename, "r+")
        self.config_file_lock = threading.Lock()

        self.sync_config()

    def __getitem__(self, key: str) -> Any:
        self.sync_config()
        return self.config[key]

    def sync_config(self) -> None:
        with self.config_file_lock:
            self.config = json.load(self.config_file)

    def save_config(self) -> None:
        with self.config_file_lock:
            json.dump(self.config, self.config_file, indent=2)

    def add_admin(self, user_id) -> None:
        self.config["default_admins"].append(user_id)
        self.save_config()

    def remove_admin(self, user_id) -> None:
        if user_id in self.config["default_admins"]:
            self.config["default_admins"].remove(user_id)
            self.save_config()
