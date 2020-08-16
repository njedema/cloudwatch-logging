import unittest
import logging
from cloudwatch_logging import CloudwatchLogging

class TestCloudwatchLogger(unittest.TestCase):
    def test_logger(self):
        context = CloudwatchLogging.LambdaContext()
        context.function_name = "TestLambdaFunction"
        context.aws_request_id = "Is finally stored in logs"
        lambda_logger = CloudwatchLogging.getLogger(__name__, runtime=CloudwatchLogging.RuntimeEnvs.LAMBDA, context=context)
        lambda_logger.setLevel(logging.INFO)
        lambda_logger.warning("Testing Lambda Adapter: request id...", extra={"field": "value"})

if __name__ == '__main__':
    unittest.main()
