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
from cloudwatch_logging import CloudwatchLogging, Filters

# create a structured JSON logger that works well with Cloudwatch and others; optionally with runtime specific appenders and filters to remove unwanted fields
logger = CloudwatchLogging.create_logger(__name__, appender=None, filter=None)
logger.setLevel(logging.INFO)
logger.warning("Structured logging with custom fields", extra={"custom_field": "custom_value"})

# add a LogTrimmer on the logger and save some money on CW storage costs
logger.addFilter(CloudwatchLogging.LogFilter(Filters.COST_EFFECTIVE))
logger.warning("Structured logging with Lambda context on the cheap!", extra={"field": "value"})
```

#### Lambda 
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# Setup logging
logger = CloudwatchLogging.create_logger("your_lambda_function")
logger.setLevel(logging.INFO)

def your_lambda_handler(event, context):
    # Lambda context changes with each invocation. Use update_context so that you can reuse your logger across invokes!
    lamdbda_appender = CloudwatchLogging.LogAppender(context)
    logger.addFilter(lamdbda_appender)
    logger.info("This line will be logged with info from the Lambda context object!", extra={"tapped_in": True})
    logger.removeFilter(lamdbda_appender)  # ensure you do this so you don't add duplicate appenders on the same logger
```

# Development
## Setup 
This is a pure Python library; it can easily be installed using `pip install cloudwatch_logging`. Use the `-e` arg if you 
plan to develop locally.

## Test
Run python3 test_cloudwatch_logging.py. Inspect the output to see what is logged. Someone should write proper tests
but I wrote this on vacation and couldn't be bothered. 

## To-Do
- Check error and exception trace handling - how can we make these better? 
- Add examples for other AWS runtimes (Fargate?)