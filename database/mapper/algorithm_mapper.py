from database.dto.algorithm_dto import AlgorithmDTO
from database.entity.algorithm_entity import AlgorithmEntity


class AlgorithmMapper:
    @staticmethod
    def entity_to_dto(entity: AlgorithmEntity) -> AlgorithmDTO:
        return AlgorithmDTO(
            id=entity.id,
            name=entity.name,
            type=entity.type,
            key_size=entity.key_size
        )

    @staticmethod
    def dto_to_entity(dto: AlgorithmDTO) -> AlgorithmEntity:
        return AlgorithmEntity(
            id=dto.id,
            name=dto.name,
            type=dto.type,
            key_size=dto.key_size
        )