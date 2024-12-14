import logging
import os

from pythonjsonlogger.jsonlogger import JsonFormatter

from rpgram_setup.presentation.middlewares import log_context


class ContextFilter(logging.Filter):
    def filter(self, record):
        log_data = log_context.get()
        record.playerId = int(log_data["player_id"])
        record.requestId = str(log_data["request_id"])
        return True


def configure_logs():
    logger = logging.getLogger()
    log_level = int(os.environ["LOG_LEVEL"])
    logger.setLevel(log_level)
    logHandler = logging.StreamHandler()
    logHandler.addFilter(ContextFilter())
    formatter = JsonFormatter("%(levelname)s %(requestId)s %(playerId)d %(message)s")
    logHandler.setFormatter(formatter)
    logHandler.setLevel(log_level)
    logger.handlers = [logHandler]
