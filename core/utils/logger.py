import sys
from loguru import logger
from core.config import settings

def setup_logging():
    """Configures the logging system."""
    logger.remove() # Remove default handler

    # Console handler (clean and informative)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # File handler (detailed for debugging)
    log_file = settings.LOGS_DIR / "bot_{time:YYYY-MM-DD}.log"
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days"
    )

    logger.info("Logging system initialized.")

if __name__ == "__main__":
    setup_logging()
    logger.info("Test log message.")
