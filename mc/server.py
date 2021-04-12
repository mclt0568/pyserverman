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
        self.server_process = subprocess.Popen(
            shlex.split(self.script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=os.path.join(self.config["servers_dir"], self.name)
        )

        try:
            while True:
                # blocking when no content is in stdout
                stdout_line_bytes = self.server_process.stdout.readline()
                if stdout_line_bytes == b"" and self.server_process.poll() is None:
                    break

                print(str(stdout_line_bytes))
        except KeyboardInterrupt:
            self.logger.log("Received terminate signal!")
            self.logger.log("Terminating subprocesses . . . ")
            self.server_process.terminate()
            self.logger.log("Terminated all subprocesses!")

    def run_command(self, command: str):
        self.server_process.stdin.write(f"{command}\r\n".encode())
        self.server_process.stdin.flush()
