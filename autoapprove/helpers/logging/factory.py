from logging import Logger, FileHandler, StreamHandler, NullHandler
from helpers.logging.formatter import default_formatter
from sys import stdout


def create_logger(logger: Logger, level: int, use_console: bool, use_file: bool, file: str) -> Logger:
    logger.setLevel(level)
    if use_console:
        console_handler: StreamHandler = StreamHandler(stream=stdout)
        console_handler.setFormatter(default_formatter)
        logger.addHandler(console_handler)
    if use_file:
        file_handler: FileHandler = FileHandler(file, mode='w', encoding='utf-8')
        file_handler.setFormatter(default_formatter)
        logger.addHandler(file_handler)

    if not (use_console or use_file):
        logger.addHandler(NullHandler())
    return logger
