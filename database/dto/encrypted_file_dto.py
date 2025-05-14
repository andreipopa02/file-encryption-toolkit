from datetime import datetime
from typing import Optional


class EncryptedFileDTO:
    def __init__(self,
                 file_name: str,
                 encrypted_path: str,
                 hash: str,
                 algorithm_id: int,
                 key_id: int,
                 created_at: datetime,
                 id: Optional[int] = None):

        self.id = id
        self.file_name = file_name
        self.encrypted_path = encrypted_path
        self.hash = hash
        self.algorithm_id = algorithm_id
        self.key_id = key_id
        self.created_at = created_at