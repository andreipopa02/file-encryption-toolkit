from database.dto.encrypted_file_dto import EncryptedFileDTO
from database.entity.encrypted_file_entity import EncryptedFileEntity


class EncryptedFileMapper:
    @staticmethod
    def entity_to_dto(entity: EncryptedFileEntity) -> EncryptedFileDTO:
        return EncryptedFileDTO(
            id=entity.id,
            file_name=entity.file_name,
            encrypted_path=entity.encrypted_path,
            hash=entity.hash,
            algorithm_id=entity.algorithm_id,
            key_id=entity.key_id,
            created_at=entity.created_at
        )

    @staticmethod
    def dto_to_entity(dto: EncryptedFileDTO) -> EncryptedFileEntity:
        return EncryptedFileEntity(
            id=dto.id,
            file_name=dto.file_name,
            encrypted_path=dto.encrypted_path,
            hash=dto.hash,
            algorithm_id=dto.algorithm_id,
            key_id=dto.key_id,
            created_at=dto.created_at
        )
