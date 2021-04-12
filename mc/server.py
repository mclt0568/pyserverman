from common import logging
import subprocess
import shlex
import common
import os
import threading


class Server(threading.Thread):
    name: str
    script: str
    config: common.Config
    logger: logging.Logger
    
    server_process: subprocess.Popen

    def __init__(self, name: str, script: str, config: common.Config, logger: logging.Logger) -> None:
        super().__init__(daemon=True)

        self.name = name
        self.script = script
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.log(f"Started server: {self.name}")
        self.server_process = subprocess.Popen(
            shlex.split(self.script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=os.path.join(self.config["servers_dir"], self.name)
        )
        while True:
            if not self.is_running():
                self.logger.log(f"Server has stopped: {self.name}")
                break

    def run_command(self, command: str):
        self.logger.log(f"Executed command on {self.name}: {command}")
        self.server_process.stdin.write(f"{command}\r\n".encode())
        self.server_process.stdin.flush()

    def is_running(self):
        stdout_line_bytes = self.server_process.stdout.readline()
        return stdout_line_bytes != b"" or self.server_process.poll() == None

    def terminate(self):
        self.logger.log(f"Server terminated manually: {self.name}")
        self.server_process.terminate()