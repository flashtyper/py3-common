import logging
from enum import Enum


class LoggingLevels(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    NOTSET = logging.NOTSET


class Logger:
    # Logging class for various applications
    def __init__(self, name: str):
        self.log = logging.getLogger(name)
        logging.basicConfig(encoding='utf-8', level=logging.INFO, format='[%(levelname)s %(asctime)s - %(name)s %(funcName)s %(lineno)s] %(message)s', datefmt='[%d.%m.%Y %H:%M:%S]')

    def __concat_msgs(msgs: Union[str, list], delimiter=',') -> str:
        if isinstance(msgs, str):
            return str
        elif isinstance(msgs, list):
            return "{delimiter} ".join([str(msg) for msg in msgs])
        else:
            raise ValueError(f"Datatype {type(msgs)} not allowed here: Only str or list!")

    def change_level(self, level: LoggingLevels):
        self.log.setLevel(level.value)
        self.log.log(level.value, 'Changed to level {}'.format(level.name))

    def info(self, *messages):
        self.log.info(messages)

    def warning(self, *messages: str):
        self.log.warning(messages)

    def error(self, *messages: str):
        self.log.error(messages)

    def critical(self, *messages: str):
        self.log.critical(messages)

    def fatal(self, *messages: str):
        self.log.fatal(messages)

    def debug(self, *messages: str):
        self.log.debug(messages)
