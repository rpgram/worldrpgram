import logging

from pythonjsonlogger.jsonlogger import JsonFormatter


def get_logger(mod: str) -> logging.Logger:
    return logging.getLogger(f"uvicorn.{mod}")


def configure_logs():
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)
    logHandler = logging.StreamHandler()
    formatter = JsonFormatter()
    logHandler.setFormatter(formatter)
    logHandler.setLevel(logging.DEBUG)
    logger.handlers = [logHandler]
