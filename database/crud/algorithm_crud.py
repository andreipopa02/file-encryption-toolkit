from sqlalchemy.orm import Session
from database.dto.algorithm_dto import AlgorithmDTO
from database.entity.algorithm_entity import AlgorithmEntity
from database.mapper.algorithm_mapper import AlgorithmMapper


class AlgorithmCRUD:

    @staticmethod
    def create_algorithm(db: Session, dto: AlgorithmDTO) -> AlgorithmDTO:
        entity = AlgorithmMapper.dto_to_entity(dto)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return AlgorithmMapper.entity_to_dto(entity)

    @staticmethod
    def get_algorithm(db: Session, algorithm_id: int) -> AlgorithmDTO:
        entity = db.query(AlgorithmEntity).filter(AlgorithmEntity.id == algorithm_id).first()
        return AlgorithmMapper.entity_to_dto(entity) if entity else None

    @staticmethod
    def update_algorithm(db: Session, algorithm_id: int, dto: AlgorithmDTO) -> AlgorithmDTO:
        entity = db.query(AlgorithmEntity).filter(AlgorithmEntity.id == algorithm_id).first()
        if not entity:
            return None

        entity.name = dto.name
        entity.type = dto.type
        entity.key_size = dto.key_size
        db.commit()
        db.refresh(entity)
        return AlgorithmMapper.entity_to_dto(entity)

    @staticmethod
    def delete_algorithm(db: Session, algorithm_id: int) -> bool:
        entity = db.query(AlgorithmEntity).filter(AlgorithmEntity.id == algorithm_id).first()
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True