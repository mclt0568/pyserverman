import subprocess
from typing import List
import shlex


class Server:
    script: str

    stdout_lines: List[str]

    def __init__(self, script: str) -> None:
        self.script = script

    def run(self) -> int:
        proc = subprocess.Popen(
            shlex.split(self.script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        while True:
            stdout_line = proc.stdout.readline()
            if stdout_line == "" and proc.poll() is not None:
                break
            self.stdout_lines.append(stdout_line)

        return proc.poll()
