from typing import Any, Dict, IO
import json
import os
import threading


class Config:
    config: Dict[str, Any]
    config_filename: str

    # config_file: IO
    config_file_lock: threading.Lock

    def __init__(self) -> None:
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
            ],
            "admins": []
        }
        self.config_filename = "config.json"

        self.config_file_lock = threading.Lock()
        if not os.path.isfile(self.config_filename):
            open(self.config_filename, "w+", encoding="utf8").close()
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
            with open(self.config_filename, "w+", encoding="utf8") as config_file:
                json.dump(self.config, config_file, indent=4)

    def add_admin(self, user_id: str, save: bool = True) -> None:
        if user_id not in self.config["admins"]:
            self.config["admins"].append(user_id)
        if save:
            self.save_config()

    def remove_admin(self, user_id: str, save: bool = True) -> None:
        if user_id in self.config["admins"]:
            self.config["admins"].remove(user_id)
            if save:
                self.save_config()
