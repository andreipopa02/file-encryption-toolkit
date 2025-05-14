from database.dto.algorithm_dto import AlgorithmDTO
from database.dto.key_dto import KeyDTO
from database.dto.encrypted_file_dto import EncryptedFileDTO
from database.dto.performance_log_dto import PerformanceLogDTO
from database.crud.algorithm_crud import AlgorithmCRUD
from database.crud.key_crud import KeyCRUD
from database.crud.encrypted_file_crud import EncryptedFileCRUD
from database.crud.performance_log_crud import PerformanceLogCRUD

from database.database import SessionLocal, get_db

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
from datetime import datetime

def generateKeyRSA(db):
    key = RSA.generate(2048)
    private_key = key.export_key()

    with open("keys/key.pem", "w") as key_file:
        key_file.write(private_key.decode('utf-8'))
    
    public_key = key.publickey().export_key()

    with open("keys/public.pem", "w") as key_file:
        key_file.write(public_key.decode('utf-8'))

    key_dto = KeyDTO(id=None, algorithm_id=0, key_type="asymmetric", key_framework="PyCryptodome", public_key=public_key.decode('utf-8'), private_key=private_key.decode('utf-8'), created_at=datetime.now())
    key = KeyCRUD.create_key(db, key_dto)
    
    print("RSA key successfully generated!")
    return key.id, public_key.decode('utf-8')

def generateKeyAES(db):
    key = get_random_bytes(32)

    with open("keys/keyfile.txt", "w") as key_file:
        key_file.write(key.hex())

    key_string = key.hex()

    key_dto = KeyDTO(
        id=None,
        algorithm_id=1,
        key_type="symmetric",
        key_framework="PyCryptodome",
        public_key=None,
        private_key=key.hex(),
        created_at=datetime.now())
    key = KeyCRUD.create_key(db, key_dto)

    print("AES key successfully generated and saved!")
    return key.id, key_string