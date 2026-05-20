"""
Logging configuration for the trading bot.

Sets up file and console logging with timestamps, levels, and formatting.
"""

import logging
import os


def setup_logging(log_dir: str = "logs", log_file: str = "trading_bot.log") -> logging.Logger:
    """
    Configure and return the application logger.

    Args:
        log_dir: Directory to store log files.
        log_file: Name of the log file.

    Returns:
        Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_file)

    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    # File handler — captures everything (DEBUG and above)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_format)

    # Console handler — INFO and above only
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)-8s %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
