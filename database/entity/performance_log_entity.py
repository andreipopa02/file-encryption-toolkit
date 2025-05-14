from sqlalchemy import Column, Integer, Enum, ForeignKey, Float, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.database import Base


class PerformanceLogEntity(Base):
    __tablename__ = 'performance_logs'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    operation           = Column(Enum('encryption', 'decryption', name='operation_type'), nullable=False)
    file_id             = Column(Integer, ForeignKey('encrypted_files.id'), nullable=False)
    algorithm_id        = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    key_id              = Column(Integer, ForeignKey('keys.id'), nullable=False)
    execution_time_ms   = Column(Float, nullable=False)
    memory_usage_kb     = Column(Float, nullable=False)
    created_at          = Column(TIMESTAMP, default=func.current_timestamp())

    file        = relationship("EncryptedFileEntity",   back_populates="performance_logs")
    algorithm   = relationship("AlgorithmEntity",       back_populates="performance_logs")
    key         = relationship("KeyEntity",             back_populates="performance_logs")