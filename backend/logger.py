"""
Structured logging configuration with JSON support
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields"""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        """Add custom fields to log record"""
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record['timestamp'] = datetime.utcnow().isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add logger name
        log_record['logger'] = record.name

        # Add source location
        log_record['source'] = f"{record.filename}:{record.lineno}"

        # Add function name
        if record.funcName:
            log_record['function'] = record.funcName

        # Add extra context if available
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id
        if hasattr(record, 'room_name'):
            log_record['room_name'] = record.room_name


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for text logs"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        """Format log record with colors"""
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"

        # Format message
        formatted = super().format(record)

        # Reset color
        record.levelname = levelname

        return formatted


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: str = None
):
    """
    Configure application logging

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type (json or text)
        log_file: Optional file path for log output
    """
    # Convert string level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Choose formatter based on format type
    if log_format.lower() == "json":
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        # Text format with colors
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Always use JSON for file output
        if log_format.lower() == "json":
            file_handler.setFormatter(formatter)
        else:
            json_formatter = CustomJsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s'
            )
            file_handler.setFormatter(json_formatter)

        root_logger.addHandler(file_handler)

    # Silence noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized: level={log_level}, format={log_format}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)


class LogContext:
    """Context manager for adding contextual information to logs"""

    def __init__(self, **kwargs):
        self.context = kwargs
        self.old_factory = None

    def __enter__(self):
        """Add context to log records"""
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record

        logging.setLogRecordFactory(record_factory)
        self.old_factory = old_factory
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original factory"""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


# Usage examples:
"""
# Initialize logging
setup_logging(log_level="INFO", log_format="json")

# Get logger
logger = get_logger(__name__)

# Basic logging
logger.info("User logged in", extra={"user_id": "123"})
logger.error("Failed to connect", extra={"error": "Connection timeout"})

# With context
with LogContext(request_id="abc-123", user_id="456"):
    logger.info("Processing request")  # Will include request_id and user_id
    logger.debug("Step 1 complete")
"""
