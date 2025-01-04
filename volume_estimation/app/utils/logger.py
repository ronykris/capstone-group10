import logging
import logging.handlers
import os
from pathlib import Path
from .config import settings

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(settings.logging.level)

    # Create formatters
    formatter = logging.Formatter(settings.logging.format)

    # Configure file handler
    if settings.logging.file["enabled"]:
        file_handler = logging.handlers.RotatingFileHandler(
            settings.logging.file["path"],
            maxBytes=settings.logging.file["max_size"] * 1024 * 1024,
            backupCount=settings.logging.file["backup_count"]
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Configure console handler
    if settings.logging.console["enabled"]:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Set logging level for external libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)