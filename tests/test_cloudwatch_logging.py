import unittest
import logging
from cloudwatch_logging import CloudwatchLogging, Filters


class TestCloudwatchLogger(unittest.TestCase):
    def test_logger(self):
        context = {"function_name": "TestLambdaFunction", "aws_request_id": "123a1a12-1234-1234-1234-123456789012"}

        # create configured logger, optionally with runtime specific appenders and filters to remove unwanted fields
        logger = CloudwatchLogging.create_logger(__name__, appender=None, filter=None)
        logger.setLevel(logging.INFO)
        logger.warning("Structured logging with custom fields", extra={"custom_field": "custom_value"})

        # create an appender that adds a configurable dict of key/values to our structured log lines
        logger.addFilter(CloudwatchLogging.LogAppender(context))
        logger.warning("Structured logging with added context from a Lambda function", extra={"field": "value"})

        # update the context used by the LogAppender
        context = {"function_name": "ProdLambdaFunction", "aws_request_id": "123a1a12-1234-1234-1234-123456789012"}
        logger.update_appender(context)
        logger.warning("Structured logging with added context from a second invoke", extra={"field": "value"})

        # enable filtering on the logger and save some money on CW storage costs
        logger.addFilter(CloudwatchLogging.LogFilter(Filters.COST_EFFECTIVE))
        logger.warning("Structured logging with Lambda context on the cheap!", extra={"field": "value"})

if __name__ == '__main__':
    unittest.main()
