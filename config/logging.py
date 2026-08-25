"""
WatchSphere AI v3.0 - Logging Configuration
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import sys
from pathlib import Path
from config.settings import settings

try:
    from loguru import logger
    
    # Automatically create logs directory if it doesn't exist
    LOG_DIR = Path(settings.LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove default Loguru handler
    logger.remove()

    # Console Logger (stdout)
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
    )

    # System Log File (Daily Rotation, 30 Days Retention)
    logger.add(
        settings.SYSTEM_LOG_FILE,
        rotation="1 day",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        encoding="utf-8",
        enqueue=True,
    )

    # Error Log File (Daily Rotation, Error Level Only)
    logger.add(
        settings.ERROR_LOG_FILE,
        rotation="1 day",
        retention="60 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
except ImportError:
    import logging
    LOG_DIR = Path(settings.LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("WatchSphereAI")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(ch)

logger.info("WatchSphere AI Enterprise Logger Initialized.")

