from typing import Any, Dict, IO
import json
import os
import threading


class Config:
    config: Dict[str, Any]
    config_filename: str

    config_file: IO
    config_file_lock: threading.Lock

    def __init__(self) -> None:
        self.config = {
            "bot": {
                "token": "",
                "guild": 0,
                "channel": 0
            },
            "server_dir": "",
            "servers": [
                {
                    "name": "",
                    "script": "",
                    "args": "",
                }
            ],
            "admins": []
        }
        self.config_filename = "config.json"

        self.config_file_lock = threading.Lock()
        if not os.path.isfile(self.config_filename):
            self.config_file = open(
                self.config_filename, "w+", encoding="utf8")
            self.save_config()
        else:
            self.config_file = open(
                self.config_filename, "r+", encoding="utf8")
            self.sync_config()

    def __del__(self):
        self.config_file.close()

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def sync_config(self) -> None:
        with self.config_file_lock:
            self.config = json.load(self.config_file)

    def save_config(self) -> None:
        with self.config_file_lock:
            json.dump(self.config, self.config_file, indent=4)
            self.config_file.flush()

    def add_admin(self, user_id: str, save: bool = True) -> None:
        self.config["admins"].append(user_id)
        if save:
            self.save_config()

    def remove_admin(self, user_id: str, save: bool = True) -> None:
        if user_id in self.config["admins"]:
            self.config["admins"].remove(user_id)
            if save:
                self.save_config()
