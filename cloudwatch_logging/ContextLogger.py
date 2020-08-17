import logging
from typing import Dict, AnyStr, Set


class ContextLogger(logging.Logger):
    def __init__(self, name, context: Dict = None):
        super().__init__(name)
        self.context = context

    def update_appender(self, append: Dict):
        self.context = append
        for filter in self.filters:
            try:
                filter.update_appender(append)
            except NameError:
                continue

    def update_filter(self, remove: Set[AnyStr]):
        self.context = remove
        for filter in self.filters:
            try:
                filter.update_filter(remove)
            except NameError:
                continue
