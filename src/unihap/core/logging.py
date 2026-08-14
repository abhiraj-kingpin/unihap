"""
==============================================================================
FILE: src/unihap/core/logging.py
MODULE: Structured Logging & Rich Console
PURPOSE:
    Configures structured, high-visibility terminal logging using RichHandler.
    Provides formatted timestamps, status spinners, and color-coded level tags.

CLASSES / OBJECTS:
    - console: Singleton Rich Console instance.
    - logger: Configured application-wide logger.

FUNCTIONS:
    - setup_logger(name: str) -> logging.Logger: Configures and returns a Rich logger.
==============================================================================
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

from unihap.config import settings

console = Console()


def setup_logger(name: str = "unihap") -> logging.Logger:
    """Configures and returns a rich-formatted logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
        handler = RichHandler(console=console, rich_tracebacks=True, markup=True, show_time=True, show_path=False)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


logger = setup_logger()
