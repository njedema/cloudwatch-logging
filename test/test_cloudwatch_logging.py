import unittest
from src.cloudwatch_logging import *


class TestCloudwatchLogger(unittest.TestCase):

    def test_logger(self):
        context = LambdaContext()
        context.function_name = "TestLambdaFunction"
        context.aws_request_id = "Is finally stored in logs"
        lambda_logger = CloudwatchLogging.getLogger(__name__, runtime=RuntimeEnvs.LAMBDA, context=context)
        lambda_logger.setLevel(logging.INFO)
        lambda_logger.warning("Testing Lambda Adapter: request id...", extra={"field": "value"})

if __name__ == '__main__':
    unittest.main()
