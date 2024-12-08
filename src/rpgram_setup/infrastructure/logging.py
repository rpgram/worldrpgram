import logging
import os

from pythonjsonlogger.jsonlogger import JsonFormatter


def configure_logs():
    logger = logging.getLogger()
    log_level = int(os.environ['LOG_LEVEL'])
    logger.setLevel(log_level)
    logHandler = logging.StreamHandler()
    formatter = JsonFormatter("%(levelname)s %(message)s")
    logHandler.setFormatter(formatter)
    logHandler.setLevel(log_level)
    logger.handlers = [logHandler]
