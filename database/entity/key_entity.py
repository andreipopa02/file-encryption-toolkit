from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.database import Base


class KeyEntity(Base):
    __tablename__ = 'keys'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    algorithm_id    = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    key_type        = Column(Enum('symmetric', 'asymmetric', name='key_type'), nullable=False)
    key_framework   = Column(Enum('OpenSSL', 'PyCryptodome', name='key_framework'), nullable=False)
    public_key      = Column(Text, nullable=True)
    private_key     = Column(Text, nullable=True)
    created_at      = Column(TIMESTAMP, default=func.current_timestamp())

    algorithm           = relationship("AlgorithmEntity",       back_populates="keys")
    encrypted_files     = relationship("EncryptedFileEntity",   back_populates="key")
    performance_logs    = relationship("PerformanceLogEntity",  back_populates="key")