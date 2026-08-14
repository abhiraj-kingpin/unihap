"""
Structured logging configuration using Rich for high-visibility terminal output.
"""

import logging
from rich.logging import RichHandler
from rich.console import Console
from unihap.config import settings

console = Console()

def setup_logger(name: str = "unihap") -> logging.Logger:
    """Configures and returns a rich-formatted logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False
        )
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

logger = setup_logger()
