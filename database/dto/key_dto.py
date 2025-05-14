from datetime import datetime
from typing import Optional


class KeyDTO:
    def __init__(self,
                 id: int,
                 algorithm_id: int,
                 key_type: str,
                 key_framework: str,
                 public_key: Optional[str],
                 private_key: Optional[str],
                 created_at: datetime):

        self.id = id
        self.algorithm_id = algorithm_id
        self.key_type = key_type
        self.key_framework = key_framework
        self.public_key = public_key
        self.private_key = private_key
        self.created_at = created_at