import json
import time
import logging
from enum import Enum
from typing import Union, AnyStr, Set
from aws_lambda_context import LambdaContext


class JSONFilter(object):
    LOW_COST = {"name", "args", "filename", "module", "thread", "threadName", "processName", "process"}
    NONE = set()

    @classmethod
    def register_filter(cls, name: AnyStr, values: Set[AnyStr]):
        setattr(JSONFilter, name, values)


class JSONFormatter(logging.Formatter):
    """
    CloudWatch supports structured JSON logging by default; this class defines a formatter that leverages logging
    builtins to extract log metadata from logs written using the native syntax. It does this by leveraging the
    behavior of the LogRecord class, which stores everything passed in "extra" as an attribute on the LogRecord.
    Its easiest for users to just pass a dict of their structured log lines, which we then figure out.
    """
    def __init__(self, filter: Set[AnyStr] = None):
        super().__init__()
        self._filter = self.update_filter(filter) if filter else JSONFilter.NONE

    def update_filter(self, filter: Set[AnyStr]):
        self._filter = filter

    def format(self, record: logging.LogRecord):
        event = {key: record.__dict__[key] for key in record.__dict__ if key not in self._filter}
        strtime = (time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)))
        event["utc_time"] = f"{strtime}.{record.msecs:3.0f}Z"
        event["timestamp"] = record.created
        return json.dumps(event)


class LambdaAdapter(logging.LoggerAdapter):
    """
    This adapter is used to extract RequestId and similarly useful fields from the Lambda context object
    """
    def __init__(self, logger: logging.Logger, context: LambdaContext):
        super().__init__(logger, extra={})
        self.update_context(context)

    def process(self, msg, kwargs):
        if hasattr(self, "_context"):  # only add context if its been set
            kwargs['extra'] = kwargs.get("extra", {})
            kwargs['extra'].update(self._context.__dict__)
        return msg, kwargs

    def update_context(self, context: LambdaContext):
        self._context = context

class AWSRuntime(Enum):
    LAMBDA = "lambda"
    NONE = None


def getLogger(name, runtime: AWSRuntime = AWSRuntime.NONE, context = None):
    # TODO make sure that this returns the existing logger/formatter/adapter when it already exists
    # TODO maybe just return an adapter always?
    logger = logging.getLogger(name)
    formatter = JSONFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if runtime is AWSRuntime.LAMBDA:
        adapter = LambdaAdapter(logger, context)
        adapter.propagate = False  # ensure we don't double log messages from lambda builtin logger
        return adapter
    else:
        return logger

def update_filter(logger: Union[logging.Logger, logging.LoggerAdapter], filter: JSONFilter):
    log = logger.logger if isinstance(logger, logging.LoggerAdapter) else logger
    if log.hasHandlers():
        for hdlr in log.handlers:
            if hasattr(hdlr, "formatter"):
                if isinstance(hdlr.formatter, JSONFormatter):
                    hdlr.formatter.update_filter(filter)
                else:
                    logging.warning("No JSONFormatter defined on this logger's handler! Create a JSONFormatter() and set"
                                    "it as your handler. Optionally, set the filter on init using the 'filter' kwarg")

    else:
        raise AttributeError("No handler defined on this logger! Please add a handler with a JSONFormatter")
