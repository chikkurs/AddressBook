import logging
import os
from datetime import datetime

# Create log folders for each log level
for level in ["INFO", "WARNING", "ERROR"]:
    os.makedirs(f"logs/{level}", exist_ok=True)

# Current date used as log file name
today = datetime.now().strftime("%Y-%m-%d")


# Custom filter to allow only a specific log level
class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    # Return True only if the log record matches the configured level
    def filter(self, record):
        return record.levelname == self.level


# Create and configure a logger instance
def get_logger(name: str = "app"):
    logger = logging.getLogger(name)

    # Prevent duplicate handlers when logger is imported multiple times
    if logger.handlers:
        return logger

    # Capture all logs; filtering is handled by individual handlers
    logger.setLevel(logging.DEBUG)

    # Common log message format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Handler for INFO logs
    info_handler = logging.FileHandler(
        f"logs/INFO/{today}.log",
        encoding="utf-8"
    )
    info_handler.addFilter(LevelFilter("INFO"))
    info_handler.setFormatter(formatter)

    # Handler for WARNING logs
    warning_handler = logging.FileHandler(
        f"logs/WARNING/{today}.log",
        encoding="utf-8"
    )
    warning_handler.addFilter(LevelFilter("WARNING"))
    warning_handler.setFormatter(formatter)

    # Handler for ERROR logs
    error_handler = logging.FileHandler(
        f"logs/ERROR/{today}.log",
        encoding="utf-8"
    )
    error_handler.addFilter(LevelFilter("ERROR"))
    error_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    return logger