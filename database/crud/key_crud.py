from sqlalchemy.orm import Session
from database.entity.key_entity import KeyEntity
from database.dto.key_dto import KeyDTO
from database.mapper.key_mapper import KeyMapper


class KeyCRUD:

    @staticmethod
    def create_key(db: Session, dto: KeyDTO) -> KeyDTO:
        entity = KeyMapper.dto_to_entity(dto)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return KeyMapper.entity_to_dto(entity)

    @staticmethod
    def get_key(db: Session, key_id: int) -> KeyDTO:
        entity = db.query(KeyEntity).filter(KeyEntity.id == key_id).first()
        return KeyMapper.entity_to_dto(entity) if entity else None

    @staticmethod
    def update_key(db: Session, key_id: int, dto: KeyDTO) -> KeyDTO:
        entity = db.query(KeyEntity).filter(KeyEntity.id == key_id).first()
        if not entity:
            return None

        entity.algorithm_id = dto.algorithm_id
        entity.key_type = dto.key_type
        entity.public_key = dto.public_key
        entity.private_key = dto.private_key
        db.commit()
        db.refresh(entity)
        return KeyMapper.entity_to_dto(entity)

    @staticmethod
    def delete_key(db: Session, key_id: int) -> bool:
        entity = db.query(KeyEntity).filter(KeyEntity.id == key_id).first()
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True
