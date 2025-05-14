from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.database import Base


class EncryptedFileEntity(Base):
    __tablename__ = 'encrypted_files'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    file_name       = Column(String(255), nullable=False)
    encrypted_path  = Column(String(255), nullable=False)
    hash            = Column(String(64), nullable=False)
    algorithm_id    = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    key_id          = Column(Integer, ForeignKey('keys.id'), nullable=False)
    created_at      = Column(TIMESTAMP, default=func.current_timestamp())

    algorithm           = relationship("AlgorithmEntity",       back_populates="encrypted_files")
    key                 = relationship("KeyEntity",             back_populates="encrypted_files")
    performance_logs    = relationship("PerformanceLogEntity",  back_populates="file")