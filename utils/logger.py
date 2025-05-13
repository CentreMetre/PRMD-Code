import logging
from config import config


def setup_logger():
    """
    Set up the logger for the application.
    """
    level = logging.DEBUG if config.VERBOSE_LOGGING else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")
