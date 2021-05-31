import os
import shlex
import subprocess
import threading

import constants
import manlib


class Server(threading.Thread):
    def __init__(self, name: str, script: str, config: manlib.Config, logger: manlib.Logger) -> None:
        super().__init__(daemon=True)

        self.name = name
        self.script = script
        self.config = config
        self.logger = logger

        self.server_process = None

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
                if constants.bot.default_channel:
                    constants.bot.loop.create_task(
                        constants.bot.default_channel.send(
                            embed=manlib.dc.GeneralInformationEmbed(
                                title="Server has exitted",
                                description=f"The following server: {self.name} has exitted\nThis might have caused by an in-game stop command or the server has crashed.\nYou can choose to dump the log before next execution"
                            )
                        )
                    )
                break

    def run_command(self, command: str):
        self.logger.log(f"Executed command on {self.name}: {command}")
        self.server_process.stdin.write(f"{command}\r\n".encode())
        self.server_process.stdin.flush()

    def is_running(self):
        if not self.server_process:
            return False
        stdout_line_bytes = self.server_process.stdout.readline()
        return stdout_line_bytes != b"" or self.server_process.poll() == None

    def terminate(self):
        self.logger.log(f"Server terminated manually: {self.name}")
        self.server_process.terminate()
