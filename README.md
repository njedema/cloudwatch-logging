# Overview

This package provides structured JSON logging faculties designed to seamlessly interoperate with log aggregators like 
AWS Cloudwatch, ELK, and others. These faculties are provided via extension of the python's existing logging library 
and can be used as a drop in replacement. 

## Usage:
If you want to generate simple structured logs, use this package just like the Python logging library. 

If you want inject contextual information into your structured logs, add a LogAppender. This is great option if you want
 to run your application in somewhere like AWS Lambda, where you would want your logs to contain aws_request_id and other
  function specific metadata. See Use Case: AWS Lambda for more.

If you want to ensure that unwanted information is removed from your logs, use a LogFilter. Filters are 
a great way to trim the size of your log lines to cut down on logging costs. Filters can also be useful in specific log 
stacks - namely the ELK stack - that need to inject specific keys like the `type` key to index logs correctly. 
 
Filters and Appenders can be mixed and matched through your logger's addFilter and removeFilter methods. 
Appenders and Filters are both dynamically configurable via the logger's update_appender and update_filter methods.

#### Basic use: JSON logging
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# create a structured JSON logger that works well with Cloudwatch and others; optionally with runtime specific appenders and filters to remove unwanted fields
logger = CloudwatchLogging.create_logger(__name__, appender=None, filter=None)
logger.setLevel(logging.INFO)
logger.warning("Structured logging with custom fields", extra={"custom_field": "custom_value"})
```

#### Use case; AWS Lambda
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# Setup logging
logger = CloudwatchLogging.create_logger("your_lambda_function")
logger.propagate = False  # disable Lambda runtime default logger from logging these
logger.setLevel(logging.INFO)

def your_lambda_handler(event, context):
    # Lambda context changes with each invocation. Use update_context so that you can reuse your logger across invokes!
    lamdbda_appender = CloudwatchLogging.LogAppender(context)
    logger.addFilter(lamdbda_appender)
    logger.info("This line will be logged with info from the Lambda context object!", extra={"tapped_in": True})
    logger.removeFilter(lamdbda_appender)  # ensure you do this so you don't add duplicate appenders on the same logger
```


#### Use case; Cloudwatch Cost Optimization
```python
import logging
from cloudwatch_logging import CloudwatchLogging, Filters

logger = CloudwatchLogging.create_logger("your_lambda_function")
logger.setLevel(logging.INFO)

# add a LogTrimmer on the logger and save some money on CW storage costs
logger.addFilter(CloudwatchLogging.LogFilter(Filters.COST_EFFECTIVE))
logger.warning("Structured logging on the cheap!", extra={"field": "value"})
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