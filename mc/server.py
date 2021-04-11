import subprocess
from sys import stdout
from typing import List, Union
import shlex


class Server:
    stdout_lines: List[str]

    def run(self, script: str) -> int:
        proc = subprocess.Popen(
            shlex.split(script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        while True:
            stdout_line = proc.stdout.readline()
            if stdout_line == "" and proc.poll() is not None:
                break
            self.stdout_lines.append(stdout_line)

        return proc.poll()
