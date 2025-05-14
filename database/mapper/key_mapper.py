from database.dto.key_dto import KeyDTO
from database.entity.key_entity import KeyEntity


class KeyMapper:
    @staticmethod
    def entity_to_dto(entity: KeyEntity) -> KeyDTO:
        return KeyDTO(
            id=entity.id,
            algorithm_id=entity.algorithm_id,
            key_type=entity.key_type,
            key_framework=entity.key_framework,
            public_key=entity.public_key,
            private_key=entity.private_key,
            created_at=entity.created_at
        )

    @staticmethod
    def dto_to_entity(dto: KeyDTO) -> KeyEntity:
        return KeyEntity(
            id=dto.id,
            algorithm_id=dto.algorithm_id,
            key_type=dto.key_type,
            key_framework=dto.key_framework,
            public_key=dto.public_key,
            private_key=dto.private_key,
            created_at=dto.created_at
        )