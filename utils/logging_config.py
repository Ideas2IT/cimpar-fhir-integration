import logging
import os
from logging.handlers import TimedRotatingFileHandler

from .config import Logs
from utils.middleware import trace_id_var, session_id_var


class RequestFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        record.session_id = session_id_var.get()
        return True


def setup_logger() -> logging.Logger:
    try:
        log_path = os.path.join(os.getcwd(), Logs.TAIL_PATH)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logger = logging.getLogger("log")
        log_formatter = logging.Formatter(
            '%(asctime)s - session_id=%(session_id)s - trace_id=%(trace_id)s - %(pathname)20s:%(lineno)4s - '
            '%(funcName)20s() - %(levelname)s ## %(message)s')
        handler = TimedRotatingFileHandler(
            os.path.join(log_path, Logs.FILE_NAME),
            when="d",
            interval=1,
            backupCount=10)
        handler.setFormatter(log_formatter)
        if not len(logger.handlers):
            logger.addHandler(handler)
        logger.addFilter(RequestFilter())
        logger.setLevel(logging.DEBUG)
        return logger
    except Exception as e:
        print(f"logging failed: {e}")


# Set up the logger when the module is imported
simple_logger = setup_logger()

