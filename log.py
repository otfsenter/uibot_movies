import logging
from logging.handlers import RotatingFileHandler

LOG_FILENAME = 'output.log'

logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s: '
        '%(levelname)s:'
        '%(name)s:'
        '%(message)s'
    )

    file_handler = RotatingFileHandler(
        filename=LOG_FILENAME,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


set_logger()
