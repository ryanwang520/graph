import time

from ariadne.types import ExtensionSync as Extension


class QueryExecutionTimeExtension(Extension):
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None

    def request_started(self, context):
        self.start_timestamp = time.perf_counter_ns()

    def format(self, context):
        return {"execution": time.perf_counter_ns() - self.start_timestamp}
