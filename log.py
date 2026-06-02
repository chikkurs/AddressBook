import logging
import os
from datetime import datetime

# Create folders
for level in ["INFO", "WARNING", "ERROR"]:
    os.makedirs(f"logs/{level}", exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")


class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelname == self.level


def get_logger(name: str = "app"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # INFO
    info_handler = logging.FileHandler(
        f"logs/INFO/{today}.log",
        encoding="utf-8"
    )
    info_handler.addFilter(LevelFilter("INFO"))
    info_handler.setFormatter(formatter)

    # WARNING
    warning_handler = logging.FileHandler(
        f"logs/WARNING/{today}.log",
        encoding="utf-8"
    )
    warning_handler.addFilter(LevelFilter("WARNING"))
    warning_handler.setFormatter(formatter)

    # ERROR
    error_handler = logging.FileHandler(
        f"logs/ERROR/{today}.log",
        encoding="utf-8"
    )
    error_handler.addFilter(LevelFilter("ERROR"))
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    return logger