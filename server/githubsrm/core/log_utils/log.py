"""
Simple logger configuration file,
returns logger object with configured logging level & file.
"""


import logging
import os
from core.settings import BASE_DIR

FMT = "%(asctime)s:%(name)s:%(message)s"
logging.root.setLevel(logging.DEBUG)


def get_logger(
    logger_name: str, filename: str, level: int = logging.INFO
) -> logging.getLogger:
    """Simple logger configuration.
    Args:
        logger_name (str): name given to current logger.
        level (int): severity level.
        filename (str): file to throw all logs to.
    Returns:
        logging.getLogger: logger object
    """
    logs_dir = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    filename = os.path.join(logs_dir, filename)
    logger = logging.getLogger(logger_name)

    file_handler = logging.FileHandler(filename, mode="a")
    file_handler.setFormatter(logging.Formatter(FMT))
    file_handler.setLevel(level=level)

    logger.addHandler(file_handler)
    return logger
