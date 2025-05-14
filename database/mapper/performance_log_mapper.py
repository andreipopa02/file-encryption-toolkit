from database.dto.performance_log_dto import PerformanceLogDTO
from database.entity.performance_log_entity import PerformanceLogEntity


class PerformanceLogMapper:
    @staticmethod
    def entity_to_dto(entity: PerformanceLogEntity) -> PerformanceLogDTO:
        return PerformanceLogDTO(
            id=entity.id,
            operation=entity.operation,
            file_id=entity.file_id,
            algorithm_id=entity.algorithm_id,
            key_id=entity.key_id,
            execution_time_ms=entity.execution_time_ms,
            memory_usage_kb=entity.memory_usage_kb,
            created_at=entity.created_at
        )

    @staticmethod
    def dto_to_entity(dto: PerformanceLogDTO) -> PerformanceLogEntity:
        return PerformanceLogEntity(
            id=dto.id,
            operation=dto.operation,
            file_id=dto.file_id,
            algorithm_id=dto.algorithm_id,
            key_id=dto.key_id,
            execution_time_ms=dto.execution_time_ms,
            memory_usage_kb=dto.memory_usage_kb,
            created_at=dto.created_at
        )
