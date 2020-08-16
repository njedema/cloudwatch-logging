# Overview

This package provides structured JSON logging faculties designed to seamlessly interoperate with log aggregators like 
AWS Cloudwatch, ELK, and others. These faculties are provided via extension of the python's existing logging library 
and can be used as a drop in replacement. 

In addition to doing structured JSON logging, this package also provides 
LoggerAdapters that can be used to inject standardized metadata into log lines. These are extremely useful when running 
your application in managed services like AWS Lambda, where fields like aws_request_id are the only way to tie your 
application logs to those emitted by the Lambda runtime. See usage examples below 

## Usage:
If you want to generate simple structured logs, use this package just like the Python logging library. If you intend to
run your application in a specific runtime (e.g. AWS Lambda), take advantage of option to use a predefined runtime. 
Runtimes add useful context specific information to all subsequent log lines without having to specify it in "extra" explicitly. 
If you want to customize your logging even further, you can update the filter used by the logger's Formatter to strip specific keys 
from the emitted JSON. This is a great way to save money on log storage costs. This feature can also be useful in specific log 
stacks - namely the ELK stack - that need to inject specific keys like the `type` key to index logs correctly.     

#### Basic usage
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# Setup logging
logger = CloudwatchLogging.getLogger("your_logger_name")
logger.setLevel(logging.INFO)

# Log some stuff
logger.info("msg", extra={"custom field": "custom value"})

# Create and use a custom JSON filter (Optional). Note, make sure your app doesn't try to log any fields with this key 
# or they will fail to appear. 
CloudwatchLogging.JSONFilter.register_filter(name="ELK", values={"type"})
CloudwatchLogging.update_filter(logger, filter=CloudwatchLogging.JSONFilter.ELK)
logger.info("Sorry to hear you haven't migrated to Cloudwatch yet", extra={"type": "will be omitted"})

# Use author recommended JSON filter; save $$$ on log storage costs, spend more on GPUs
CloudwatchLogging.update_filter(logger, filter=CloudwatchLogging.JSONFilter.LOW_COST)
logger.info("This line costs less", extra={"custom_field": "custom_value"})
```

#### Lambda 
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# Setup logging
logger = CloudwatchLogging.getLogger("your_lambda_function", runtime=CloudwatchLogging.AWSRuntime.LAMBDA)
logger.setLevel(logging.INFO)

def your_lambda_handler(event, context):
    # Lambda context changes with each invocation. Use update_context so that you can reuse your logger across invokes!   
    logger.update_context(context=context)
    logger.info("This line will be logged with info from the Lambda context object!", extra={"tapped_in": True})
```

# Development
## Setup 
This is a pure Python library; it can easily be installed using `pip install cloudwatch_logging`. Use the `-e` arg if you 
plan to develop locally.

## Test
Run python3 test_cloudwatch_logging.py. Inspect the output to see what is logged. Someone should write proper tests
but I wrote this on vacation and couldn't be bothered. 

## To-Do
- Ensure getLogger works with existing loggers/adapters -> maybe use Adapter for everything to standardize
- Check error and exception trace handling - how can we make these better? 
- Add support for other AWS runtimes (Fargate?)