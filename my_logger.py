from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod 


class LogSettings:
    """
    Settings for log formatting.
    """
    def __init__(self, timestamp_format: str, info_msg_sep: str, inter_info_sep: str):
        """
        Initialize log settings.

        :param timestamp_format: The format for the timestamp.
        :param info_msg_sep: Separator between log information and message.
        :param inter_info_sep: Separator between bullet string and timestamp.
        """
        self.timestamp_format = timestamp_format
        self.info_msg_sep = info_msg_sep
        self.inter_info_sep = inter_info_sep


DEFAULT_LOG_SETTINGS = LogSettings(
    timestamp_format="[%d/%m/%Y, %H:%M:%S]",
    info_msg_sep=" :   ",
    inter_info_sep=" | "
)


class LogType:
    """
    Represents a log type with display string and bullet string.
    """
    def __init__(self, display_str: str, bullet_str: str):
        """
        Initialize a LogType with a display string and a bullet string.

        :param display_str: Display string for the log type.
        :param bullet_str: Bullet string for the log type.
        """
        self.display_str = display_str
        self.bullet_str = bullet_str

    def __eq__(self, other):
        return (self.display_str == other.display_str) and (self.bullet_str == other.bullet_str)


class LOG_TYPES:
    DEBUG   = LogType("[DEBUG__]", "[+]")
    WARNING = LogType("[WARNING]", "[?]")
    ERROR   = LogType("[ERROR__]", "[!]")


class LogEntry:
    """
    Represents a log entry with a message, log type, and timestamp.
    """
    def __init__(self, log_message: str, log_type: LogType, timestamp: Optional[datetime] = None):
        """
        Initialize a log entry.

        :param log_message: The log message.
        :param log_type: The log type.
        :param timestamp: The timestamp for the log entry (defaults to the current time).
        """
        self.log_type = log_type
        self.log_message = log_message
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp


def parse_log_str(log_str: str, log_settings: LogSettings) -> LogEntry:
    """
    Parse a log string into a LogEntry object.

    :param log_str: The log string to parse.
    :param log_settings: The log settings for formatting.
    :return: A LogEntry object.
    :raises ValueError: If the log cannot be parsed.
    """
    try:
        log_info, _, log_msg = log_str.partition(log_settings.info_msg_sep)
        log_info_data = log_info.split(log_settings.inter_info_sep)
        log_type = LogType(log_info_data[2], log_info_data[0])
        time_stamp = datetime.strptime(log_info_data[1], log_settings.timestamp_format)
        return LogEntry(log_msg, log_type, time_stamp)
    except Exception as e:
        raise ValueError(f"Invalid Log cannot be parsed. {e}")


def create_log_message(log_entry: LogEntry, log_settings: LogSettings) -> str:
    """
    Create a log message string from a LogEntry object.

    :param log_entry: The LogEntry to format.
    :param log_settings: The log settings for formatting.
    :return: The formatted log message.
    """
    log = log_settings.inter_info_sep.join(
        [
            log_entry.log_type.bullet_str,
            log_entry.timestamp.strftime(log_settings.timestamp_format),
            log_entry.log_type.display_str
        ]
    )
    log += log_settings.info_msg_sep + log_entry.log_message
    return log


class LoggerBase(ABC):
    """
    Abstract base class for loggers.
    """
    @abstractmethod
    def log(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        pass


class FileLogger(LoggerBase):
    """
    Logger for logging to a file.
    """
    def __init__(self, file_path: str = "logs.txt", log_settings: LogSettings = DEFAULT_LOG_SETTINGS):
        """
        Initialize the FileLogger.

        :param file_path: The path to the log file.
        :param log_settings: The log settings for formatting.
        """
        self.file_path = file_path
        self.log_settings = log_settings

    def log(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        """
        Log a message to a file.

        :param message: The log message.
        :param log_type: The log type (default is DEBUG).
        """
        log_entry = LogEntry(message, log_type)
        last_log = self.get_last_log()

        if last_log and (last_log.log_type.display_str, last_log.log_type.bullet_str) != (log_type.display_str, log_type.bullet_str):
            line_prefix = "\n"
        else:
            line_prefix = ""

        log_str = line_prefix + create_log_message(log_entry, self.log_settings) + "\n"

        with open(self.file_path, "a") as log_file:
            log_file.write(log_str)

    def get_last_log(self) -> Optional[LogEntry]:
        """
        Get the last log entry from the log file.

        :return: The last log entry or None if there are no logs.
        """
        try:
            with open(self.file_path, 'r') as log_file:
                log_lines = log_file.readlines()
                if not log_lines:
                    return None

                last_line = log_lines[-1]
                if not last_line:
                    last_line = log_lines[-2]

                last_log = parse_log_str(last_line, self.log_settings)
                return last_log

        except IOError:
            return None

    def clear_logs_from_file(self):
        """
        Clear all logs from the log file.
        """
        with open(self.file_path, "w") as log_file:
            log_file.write("")


class ConsoleLogger(LoggerBase):
    """
    Logger for logging to the console.
    """
    def __init__(self, log_settings: LogSettings):
        """
        Initialize the ConsoleLogger.

        :param log_settings: The log settings for formatting.
        """
        self.log_settings = log_settings

    def log(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        """
        Log a message to the console.

        :param message: The log message.
        :param log_type: The log type (default is DEBUG).
        """
        log_entry = LogEntry(message, log_type)
        log_msg = create_log_message(log_entry, self.log_settings)
        print(log_msg)


class Logger:
    """
    Logger that combines file and console logging.
    """
    def __init__(self, file_log_path: str = "logs.txt", log_settings: LogSettings = DEFAULT_LOG_SETTINGS):
        """
        Initialize the Logger.

        :param file_log_path: The path to the log file.
        :param log_settings: The log settings for formatting.
        """
        self.file_log_path = file_log_path
        self.log_settings = log_settings
        self.file_logger = FileLogger(file_log_path, log_settings)
        self.console_logger = ConsoleLogger(log_settings)
        self.loggers = [self.file_logger, self.console_logger]

    def file_log(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        """
        Log a message to the file.

        :param message: The log message.
        :param log_type: The log type (default is DEBUG).
        """
        self.file_logger.log(message, log_type)

    def console_log(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        """
        Log a message to the console.

        :param message: The log message.
        :param log_type: The log type (default is DEBUG).
        """
        self.console_logger.log(message, log_type)

    def log_on_all(self, message: str, log_type: LogType = LOG_TYPES.DEBUG):
        """
        Log a message to both the file and console.

        :param message: The log message.
        :param log_type: The log type (default is DEBUG).
        """
        for logger in self.loggers:
            logger.log(message, log_type)

if __name__ == '__main__':
    f_logger = FileLogger()
    f_logger.clear_logs_from_file()

    try:
        for i in range(50, -5, -1):
            if 100 % i == 0:
                f_logger.log(f"{i} is a factor of 100", LOG_TYPES.WARNING)
            else:
                f_logger.log(f"{i} gives reminder {100 % i} when dividing 100", LOG_TYPES.DEBUG)
    except Exception as e:
        f_logger.log(str(e), LOG_TYPES.ERROR)
