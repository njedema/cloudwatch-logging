# Overview

This package provides structured logging faculties designed to facilitate easy log querying in CloudWatch. You can also use
this logger with any package other than These faculties 
are provided via extension of the native python logging libary. In addition to provided access to JSON formatted logging 
through native python logging syntax, this package also provides AWS Service (e.g. Lambda) specific LoggerAdapaters that allow
for the easy addition of runtime specific metadata (e.g. Lambda requestId). 

## Usage:
This package should be used just like the builtin Python logging library. The most basic use of the library is below
```python
import logging
from cloudwatch_logging import CloudwatchLogging

# Setup logging
logger = CloudwatchLogging.getLogger("your_logger_name")
logger.setLevel(logging.INFO)

# Log some stuff
logger.info("msg", extra={"custom field": "custom value"})

```

# Development
## Setup 
This is a pure Python library; it can easily be installed using `pip install cloudwatch_logging`. Use the `-e` arg if you 
plan to develop locally.

## Test
Run python3 test_cloudwatch_logging.py

## To-Do
- Add advanced examples to readMe for filtering and customization
- Check error and exception trace handling - how can we make these better? 
- Add support for other AWS runtimes (Fargate?)