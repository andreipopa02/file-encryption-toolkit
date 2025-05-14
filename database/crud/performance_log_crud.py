from sqlalchemy.orm import Session
from database.dto.performance_log_dto import PerformanceLogDTO
from database.entity.performance_log_entity import PerformanceLogEntity
from database.mapper.performance_log_mapper import PerformanceLogMapper


class PerformanceLogCRUD:

    @staticmethod
    def create_log(db: Session, dto: PerformanceLogDTO) -> PerformanceLogDTO:
        entity = PerformanceLogMapper.dto_to_entity(dto)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return PerformanceLogMapper.entity_to_dto(entity)

    @staticmethod
    def get_log(db: Session, log_id: int) -> PerformanceLogDTO:
        entity = db.query(PerformanceLogEntity).filter(PerformanceLogEntity.id == log_id).first()
        return PerformanceLogMapper.entity_to_dto(entity) if entity else None

    @staticmethod
    def update_log(db: Session, log_id: int, dto: PerformanceLogDTO) -> PerformanceLogDTO:
        entity = db.query(PerformanceLogEntity).filter(PerformanceLogEntity.id == log_id).first()
        if not entity:
            return None

        entity.operation = dto.operation
        entity.file_id = dto.file_id
        entity.algorithm_id = dto.algorithm_id
        entity.key_id = dto.key_id
        entity.execution_time_ms = dto.execution_time_ms
        entity.memory_usage_kb = dto.memory_usage_kb
        db.commit()
        db.refresh(entity)
        return PerformanceLogMapper.entity_to_dto(entity)

    @staticmethod
    def delete_log(db: Session, log_id: int) -> bool:
        entity = db.query(PerformanceLogEntity).filter(PerformanceLogEntity.id == log_id).first()
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True
