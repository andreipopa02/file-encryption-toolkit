import subprocess

from database.dto.algorithm_dto import AlgorithmDTO
from database.dto.key_dto import KeyDTO
from database.dto.encrypted_file_dto import EncryptedFileDTO
from database.dto.performance_log_dto import PerformanceLogDTO
from database.crud.algorithm_crud import AlgorithmCRUD
from database.crud.key_crud import KeyCRUD
from database.crud.encrypted_file_crud import EncryptedFileCRUD
from database.crud.performance_log_crud import PerformanceLogCRUD

from database.database import SessionLocal, get_db

import os
from datetime import datetime

def generateKeyRSA(db):
    command = ["openssl", "genrsa", "-out", "keys/key.pem", "2048"]
    try:
        subprocess.run(command, check=True)

        subprocess.run(["openssl", "rsa", "-in", "keys/key.pem", "-outform", "PEM", "-pubout", "-out", "keys/public.pem"], check=True)
        result = subprocess.run(["openssl", "rsa", "-pubin", "-in", "keys/public.pem", "-text"], capture_output=True, text=True, check=True)

        with open("keys/public.pem", "r") as pubkey_file, open("keys/key.pem", "r") as key_file:
            pubkey = pubkey_file.read()
            key = key_file.read()

            key_dto = KeyDTO(id=None, algorithm_id=0, key_type="asymmetric", key_framework="OpenSSL", public_key=pubkey, private_key=key, created_at=datetime.now())
            key = KeyCRUD.create_key(db, key_dto)

        print("RSA key successfully generated!")
        return key.id, pubkey
    except subprocess.CalledProcessError as e:
        print(f"Error generating OpenSSL RSA key: {e}")
        return False, False
    

def generateKeyAES(db):
    command = ["openssl", "rand", "-hex", "32"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        with open("keys/keyfile.txt", "w") as key_file:
            key_file.write(result.stdout.strip())

        key_dto = KeyDTO(id=None, algorithm_id=1, key_type="symmetric", key_framework="OpenSSL", public_key=None, private_key=result.stdout.strip(), created_at=datetime.now())
        key = KeyCRUD.create_key(db, key_dto)

        print("AES key successfully generated and saved!")
        return key.id, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error generating OpenSSL AES key: {e}")
        return False, False