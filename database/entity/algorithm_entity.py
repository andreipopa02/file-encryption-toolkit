from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database.database import Base


class AlgorithmEntity(Base):
    __tablename__ = 'algorithms'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(50), nullable=False)
    type        = Column(Enum('symmetric', 'asymmetric', name='algorithm_type'), nullable=False)
    key_size    = Column(Integer, nullable=False)

    keys                = relationship("KeyEntity",             back_populates="algorithm")
    encrypted_files     = relationship("EncryptedFileEntity",   back_populates="algorithm")
    performance_logs    = relationship("PerformanceLogEntity",  back_populates="algorithm")