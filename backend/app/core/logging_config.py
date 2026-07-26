import os
import sys
from loguru import logger
from backend.app.core.config import settings

def setup_logging():
    """
    Setup logging interceptors and file output rotation.
    Combines console output and rolling file logging.
    """
    # Remove existing handlers to avoid duplicates
    logger.remove()
    
    # Define log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # 1. Console Log Handler
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=log_format,
        colorize=True
    )
    
    # 2. File Log Handler (Ensure directory exists)
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format=log_format,
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        encoding="utf-8"
    )
    
    logger.info("Structured logging framework initialized.")
    return logger
