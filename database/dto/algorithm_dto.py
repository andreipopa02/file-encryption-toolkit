class AlgorithmDTO:
    def __init__(self,
                 id: int,
                 name: str,
                 type: str,
                 key_size: int):

        self.id = id
        self.name = name
        self.type = type
        self.key_size = key_size