import time
import tracemalloc
from database.dto.performance_log_dto import PerformanceLogDTO
from database.crud.performance_log_crud import PerformanceLogCRUD
from datetime import datetime

def caclculate_performances(func, encrypt, db, currentKey, *args):
    start_time = time.perf_counter()
    tracemalloc.start()

    result, message, file = func(*args)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result and file:
        log_dto = PerformanceLogDTO(
            id=None,
            operation=encrypt,
            file_id=file.id,
            algorithm_id=file.algorithm_id,
            key_id=currentKey,
            execution_time_ms=(end_time - start_time) * 1000,
            memory_usage_kb=peak / 1024,
            created_at=datetime.now()
        )
        PerformanceLogCRUD.create_log(db, log_dto)

    return result, message
