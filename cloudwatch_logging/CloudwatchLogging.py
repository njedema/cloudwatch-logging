import json
import time
import logging
from typing import Union, AnyStr, Set, Dict
from cloudwatch_logging.ContextLogger import ContextLogger


logging.setLoggerClass(ContextLogger)
logger = logging.getLogger(__name__)


class JSONFormatter(logging.Formatter):
    """
    CloudWatch supports structured JSON logging by default; this class defines a formatter that leverages logging
    builtins to extract log metadata from logs written using the native syntax. It does this by leveraging the
    behavior of the LogRecord class, which stores everything passed in "extra" as an attribute on the LogRecord.
    Its easiest for users to just pass a dict of their structured log lines, which we then figure out.
    """
    def format(self, record: logging.LogRecord):
        event = {}
        event.update(record.__dict__)
        strtime = (time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)))
        event["utc_time"] = f"{strtime}.{record.msecs:3.0f}Z"
        event["timestamp"] = record.created
        return json.dumps(event)


class LogAppender(logging.Filter):
    def __init__(self, append: Dict):
        super().__init__()
        self._content = append

    def filter(self, record: logging.LogRecord):
        if self._content:
            for attr in self._content:
                if not hasattr(record, attr):
                    record.__setattr__(attr, self._content.get(attr))
                else:
                    logger.warning(f"Appender key {attr} found in line! Not adding")
                    continue
        return True

    def update_appender(self, append: Dict):
        self._content = append


class LogFilter(logging.Filter):
    def __init__(self, remove: Set[AnyStr] = None):
        super().__init__()
        self._remove = remove if remove else {}

    def filter(self, record: logging.LogRecord):
        for attr in self._remove:
            if hasattr(record, attr):
                record.__delattr__(attr)
        return True

    def update_filter(self, remove: Set[AnyStr]):
        self._remove = remove


def create_logger(name, appender: Union[LogAppender, logging.Filter] = None, filter: Union[LogFilter, logging.Filter] = None) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = JSONFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if isinstance(appender, LogAppender) or isinstance(appender, logging.Filter):
        logger.addFilter(appender)

    if isinstance(filter, LogFilter) or isinstance(filter, logging.Filter):
        logger.addFilter(filter)

    return logger
