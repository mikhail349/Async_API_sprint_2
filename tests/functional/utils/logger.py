import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""Формат лога."""

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("tests")
