from sqlalchemy.orm import Session
from database.dto.encrypted_file_dto import EncryptedFileDTO
from database.entity.encrypted_file_entity import EncryptedFileEntity
from database.mapper.encrypted_file_mapper import EncryptedFileMapper


class EncryptedFileCRUD:

    @staticmethod
    def create_file(db: Session, dto: EncryptedFileDTO) -> EncryptedFileDTO:
        entity = EncryptedFileMapper.dto_to_entity(dto)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return EncryptedFileMapper.entity_to_dto(entity)

    @staticmethod
    def get_file(db: Session, file_id: int) -> EncryptedFileDTO:
        entity = db.query(EncryptedFileEntity).filter(EncryptedFileEntity.id == file_id).first()
        return EncryptedFileMapper.entity_to_dto(entity) if entity else None

    @staticmethod
    def get_file_by_name(db: Session, file_name: str) -> EncryptedFileDTO:
        entity = db.query(EncryptedFileEntity).filter(EncryptedFileEntity.file_name == file_name).first()
        return EncryptedFileMapper.entity_to_dto(entity) if entity else None

    @staticmethod
    def update_file(db: Session, file_id: int, dto: EncryptedFileDTO) -> EncryptedFileDTO:
        entity = db.query(EncryptedFileEntity).filter(EncryptedFileEntity.id == file_id).first()
        if not entity:
            return None

        entity.file_name = dto.file_name
        entity.encrypted_path = dto.encrypted_path
        entity.hash = dto.hash
        entity.algorithm_id = dto.algorithm_id
        entity.key_id = dto.key_id
        db.commit()
        db.refresh(entity)
        return EncryptedFileMapper.entity_to_dto(entity)

    @staticmethod
    def delete_file(db: Session, file_id: int) -> bool:
        entity = db.query(EncryptedFileEntity).filter(EncryptedFileEntity.id == file_id).first()
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True