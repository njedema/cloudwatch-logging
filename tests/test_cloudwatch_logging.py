import unittest
import logging
from cloudwatch_logging import CloudwatchLogging
from cloudwatch_logging.CloudwatchLogging import JSONFilter


class TestCloudwatchLogger(unittest.TestCase):
    def test_logger(self):
        context = CloudwatchLogging.LambdaContext()
        context.function_name = "TestLambdaFunction"
        context.aws_request_id = "123a1a12-1234-1234-1234-123456789012"
        lambda_logger = CloudwatchLogging.getLogger(__name__, runtime=CloudwatchLogging.AWSRuntime.LAMBDA, context=context)
        lambda_logger.setLevel(logging.INFO)
        lambda_logger.warning("Structured logging with Lambda context object and custom fields", extra={"field": "value"})

        # enable filtering on the Lambda logger and save some money on CW storage costs
        CloudwatchLogging.update_filter(lambda_logger, filter=JSONFilter.LOW_COST)
        lambda_logger.warning("Structured logging with useful attributes only", extra={"field": "value"})

        # define custom filtering to ensure logstash "type" key is filtered out.
        JSONFilter.register_filter(name="ELK_DEFAULT", values={"type"})
        CloudwatchLogging.update_filter(lambda_logger, filter=JSONFilter.ELK_DEFAULT)
        lambda_logger.warning("Structured logging that's compatible with the ELK stack")

if __name__ == '__main__':
    unittest.main()
