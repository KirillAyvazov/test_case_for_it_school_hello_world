from sys import stdout
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    stream=stdout,
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
