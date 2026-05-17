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


class FlicklLogger:
    def __init__(self, name: str):
        self.log = logging.getLogger(name)
        logging.basicConfig(encoding='utf-8', level=logging.INFO, format='[%(levelname)s %(asctime)s - %(name)s %(funcName)s %(lineno)s] %(message)s', datefmt='[%d.%m.%Y %H:%M:%S]')

    def change_level(self, level: LoggingLevels):
        self.log.setLevel(level.value)
        self.log.log(level.value, 'Changed to level {}'.format(level.name))

    def info(self, message: str):
        self.log.info(message)

    def warning(self, message: str):
        self.log.warning(message)

    def error(self, message: str):
        self.log.error(message)

    def critical(self, message: str):
        self.log.critical(message)

    def fatal(self, message: str):
        self.log.fatal(message)

    def debug(self, message: str):
        self.log.debug(message)
