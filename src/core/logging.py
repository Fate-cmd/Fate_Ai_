import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging
def setup_logging():
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # Create handlers
    file_handler = RotatingFileHandler(
        log_dir / "fate.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if settings.APP_DEBUG else logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.APP_DEBUG else logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    loggers = {
        "sqlalchemy.engine": logging.WARNING,
        "alembic": logging.INFO,
        "uvicorn": logging.INFO,
        "fastapi": logging.INFO,
    }

    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)

    return root_logger

# Create logger instance
logger = setup_logging() 