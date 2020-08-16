import json
import time
import logging
from enum import Enum
from typing import List, AnyStr

from aws_lambda_context import LambdaContext


class CloudwatchFormatter(logging.Formatter):
    """
    CloudWatch supports structured JSON logging by default; this class defines a formatter that leverages logging
    builtins to extract log metadata from logs written using the native syntax. It does this by leveraging the
    behavior of the LogRecord class, which stores everything passed in "extra" as an attribute on the LogRecord.
    Its easiest for users to just pass a dict of their structured log lines, which we then figure out.
    """
    DEFAULT_FILTER = ["name", "filename", "module", "thread", "threadName", "processName", "process"]

    def __init__(self, filter):
        super().__init__()
        self.update_filter(filter)

    def update_filter(self, filter_attrs: List[AnyStr]):
        self.filter = filter_attrs

    def format(self, record: logging.LogRecord):
        event = {key: record.__dict__[key] for key in record.__dict__ if key not in self.filter}
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


class RuntimeEnvs(Enum):
    LAMBDA = "lambda"
    NONE = None


def getLogger(name, runtime: RuntimeEnvs = RuntimeEnvs.NONE, context = None):
    logger = logging.getLogger(name)
    formatter = CloudwatchFormatter(CloudwatchFormatter.DEFAULT_FILTER)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if runtime is RuntimeEnvs.LAMBDA:
        adapter = LambdaAdapter(logger, context)
        adapter.propagate = False  # ensure we don't double log messages from lambda builtin logger
        return adapter

    else:
        return logger