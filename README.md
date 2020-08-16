# Overview

This package provides structured logging faculties designed to facilitate easy log querying in CloudWatch. These faculties 
are provided via extension of the native python logging libary. In addition to provided access to JSON formatted logging 
through native python logging syntax, this package also provides AWS Service (e.g. Lambda) specific LoggerAdapaters that allow
for the easy addition of runtime specific metadata (e.g. Lambda requestId, ECS task id, etc). Once created, the logger
can be easily used with: `logger.info("msg", extra={"field_name": "field_value"})` 

## Example
Use like this:
```python
from cloudwatch_logging import CloudwatchLogging

# Setup logging
LOGGER = CloudwatchLogging.getLogger("your_logger_name")
```

# Development
## Setup 
This is a pure Python library; it can easily be installed using `pip install cloudwatch_logging`

## Test
