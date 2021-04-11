from typing import Any, Dict, IO
from ColorStr import parse as colorparse
from enum import Enum
import datetime
import os
import threading


class LogLevel:
    tag: str
    color: str

    def __init__(self, tag: str, color: str) -> None:
        self.tag = tag
        self.color = color


class LogLevelName(Enum):
    LOG = "log"
    ERROR = "error"
    EXCEPTION = "exception"
    WARNING = "warning"


class Logger:
    log_directory: str
    log_filename: str

    line_prefix: str
    line_suffix: str

    log_levels: Dict[str, LogLevel]

    log_file: IO
    log_file_lock: threading.Lock

    def __init__(self) -> None:
        self.log_directory = "logs"
        self.log_filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log")

        if not os.path.isdir(self.log_directory):
            os.mkdir(self.log_directory)

        self.prefix = "[{}][{}] "
        self.suffix = "\n"

        self.log_levels = {
            LogLevelName.LOG: LogLevel("LOG", "§g"),
            LogLevelName.ERROR: LogLevel("ERR", "§r"),
            LogLevelName.EXCEPTION: LogLevel("EXC", "§r"),
            LogLevelName.WARNING: LogLevel("WRN", "§y"),
        }
        self.default_log_level = self.log_levels[LogLevelName.LOG]

        self.log_file = open(
            f"{self.log_directory}/{self.log_filename}",
            "a+",
            encoding="utf8"
        )
        self.log_file_lock = threading.Lock()

    def __del__(self) -> None:
        self.log_file.close()

    def construct_message(self, message: str, level="") -> None:
        if level and level in self.log_levels:
            log_level = self.log_levels[level]
        else:
            log_level = self.default_log_level
        log_level_tag = log_level.tag
        log_level_color = log_level.color

        date_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        file_message = self.prefix.format(date_time, log_level_tag) + message
        console_message = self.prefix.format(
            date_time, colorparse(log_level_color + log_level_tag + "§0")) + message

        return file_message, console_message

    # flush will update the log file
    # set it to false when writing frequently
    def write_to_file(self, line: str, flush: bool = True) -> None:
        with self.log_file_lock:
            self.log_file.write(line + "\n")
            if flush:
                self.flush_file()

    def flush_file(self) -> None:
        with self.log_file_lock:
            self.log_file.flush()

    def log(self, raw_message: Any, level="") -> None:
        message = str(raw_message)

        message_lines = message.split("\n")
        if message_lines and not message_lines[-1]:
            del message_lines[-1]

        log_messages = [self.construct_message(line, level=level)
                        for line in message_lines]
        if level == LogLevelName.EXCEPTION:
            log_messages = [
                self.construct_message(
                    "== UNEXPECTED EXCEPTION ==", level=LogLevelName.EXCEPTION),
                *log_messages,
                self.construct_message(
                    "==== END OF EXCEPTION ====", level=LogLevelName.EXCEPTION)
            ]

        for file_message, console_message in log_messages:
            print(console_message)
            self.write_to_file(file_message, flush=False)

        self.flush_file()
