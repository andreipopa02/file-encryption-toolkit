from datetime import datetime
from typing import Optional


class PerformanceLogDTO:
    def __init__(self,
                 operation: str,
                 file_id: int,
                 algorithm_id: int,
                 key_id: int,
                 execution_time_ms: float,
                 memory_usage_kb: float,
                 created_at: datetime,
                 id: Optional[int]= None):

        self.id = id
        self.operation = operation
        self.file_id = file_id
        self.algorithm_id = algorithm_id
        self.key_id = key_id
        self.execution_time_ms = execution_time_ms
        self.memory_usage_kb = memory_usage_kb
        self.created_at = created_at