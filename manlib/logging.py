import os
import threading
from datetime import datetime
from enum import Enum
from typing import Any, IO, List, Tuple

from ColorStr import parse as colorparse


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


class LogStream:
    def __init__(self, stream: IO, enable_color: bool = False) -> None:
        self.stream = stream
        self.enable_color = enable_color


class Logger:
    def __init__(self, output_streams: List[LogStream]) -> None:
        self.output_streams = output_streams
        self.output_streams_lock = threading.Lock()

        self.log_directory = "logs"
        self.log_filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log")

        if not os.path.isdir(self.log_directory):
            os.mkdir(self.log_directory)

        self.message_prefix = "[{}][{}] "
        self.message_suffix = "\n"

        self.log_levels = {
            LogLevelName.LOG: LogLevel("LOG", "§g"),
            LogLevelName.ERROR: LogLevel("ERR", "§r"),
            LogLevelName.EXCEPTION: LogLevel("EXC", "§r"),
            LogLevelName.WARNING: LogLevel("WRN", "§y"),
        }
        self.default_log_level = self.log_levels[LogLevelName.LOG]

    def construct_message(self, message: str, level: LogLevelName = "") -> Tuple[str, str]:
        # log level
        log_level = self.default_log_level
        if level and level in self.log_levels:
            log_level = self.log_levels[level]

        date_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        plain_message = self.message_prefix.format(
            date_time,
            colorparse(log_level.color + log_level.tag + "§0")
        ) + message + self.message_suffix
        colorized_message = self.message_prefix.format(
            date_time,
            log_level.tag
        ) + message + self.message_suffix

        return plain_message, colorized_message

    def log(self, raw_message: Any, level: LogLevelName = "") -> None:
        # message
        message = str(raw_message)
        message_lines = message.split("\n")

        log_messages = []
        if level == LogLevelName.EXCEPTION:
            self.construct_message(
                "== UNEXPECTED EXCEPTION ==", level=LogLevelName.EXCEPTION)
        for message_line in message_lines:
            log_messages.append(self.construct_message(message_line, level))
        if level == LogLevelName.EXCEPTION:
            self.construct_message(
                "==== END OF EXCEPTION ====", level=LogLevelName.EXCEPTION)

        with self.output_streams_lock:
            for plain_log_message, colorized_log_message in log_messages:
                for stream in self.output_streams:
                    if stream.enable_color:
                        stream.stream.write(colorized_log_message)
                    else:
                        stream.stream.write(plain_log_message)
                    stream.stream.flush()
