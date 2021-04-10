from typing import IO
from ColorStr import parse as colorparse
import datetime
import os


class Logger:
    log_directory: str
    log_filename: str

    line_prefix: str
    line_suffix: str

    log_file: IO

    def __init__(self) -> None:
        self.log_directory = "logs"
        self.log_filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log")

        if not os.path.isdir(self.log_directory):
            os.mkdir(self.log_directory)

        self.prefix = "[{}][{}] "
        self.suffix = "\n"

        self.modes = {
            "log": ["LOG", "§g"],
            "error": ["ERR", "§r"],
            "exception": ["EXC", "§r"],
            "warning": ["WRN", "§y"],
        }

        self.log_file = open(f"{self.log_directory}/{self.log_filename}", "w+").close()
    
    def __del__(self) -> None:
        self.log_file.close()

    def construct_message(self, message, logtype="log"):
        mode = self.modes[logtype][0] if logtype in self.modes else "LOG"
        color = self.modes[logtype][1] if logtype in self.modes else "§g"
        date = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        log_in_file = self.prefix.format(date, mode) + message
        log_in_console = self.prefix.format(
            date, colorparse(color+mode+"§0")) + message
        return log_in_file, log_in_console

    def write_to_file(self, line):
        with open(f"{self.log_directory}/{self.log_filename}", "a", encoding="utf8") as f:
            f.write(line+"\n")

    def log(self, message, logtype="log"):
        message = str(message)
        list_of_messages = message.split("\n")
        if list_of_messages:
            if not list_of_messages[-1]:
                list_of_messages = list_of_messages[:-1]
        logs = [self.construct_message(str(i), logtype=logtype)
                for i in list_of_messages]
        if logtype == "exception":
            logs = [self.construct_message("== UNEXPECTED EXCEPTION ==", logtype="exception")] + logs + [
                self.construct_message("== END OF EXCEPTION ==", logtype="exception")]
        for file, console in logs:
            print(console)
            self.write_to_file(file)
