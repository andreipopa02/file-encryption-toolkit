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
import subprocess
import hashing.hash as hashing
import time
import tracemalloc


def encryptRSA(file_path, db, currentKey):
    encrypted_file_path = (file_path + ".encrypted")
    key_file_path = encrypted_file_path + ".key"

    # Generated the AES Key
    command = ["openssl", "rand", "-hex", "32"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        with open("keys/tempAESKey.txt", "w") as key_file:
            key_file.write(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error generating OpenSSL AES key for the RSA Encryption: {e}")
        return False, "Error generating OpenSSL AES key for the RSA Encryption"

    try:
        # Encrypt the file using AES
        subprocess.run([
            "openssl", "enc", "-aes-256-cbc",
            "-in", file_path,
            "-out", encrypted_file_path,
            "-kfile", "keys/tempAESKey.txt"
        ], check=True)

        # Encrypt the AES Key using RSA
        subprocess.run([
            "openssl", "pkeyutl", "-encrypt",
            "-pubin", "-inkey", "keys/public.pem",
            "-in", "keys/tempAESKey.txt",
            "-out", key_file_path
        ], check=True)

        os.remove("keys/tempAESKey.txt")

        hash = hashing.hash_file(file_path)

        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".encrypted", "")

        file_dto = EncryptedFileDTO(file_name=file_name, encrypted_path=encrypted_file_path, hash=hash, algorithm_id=0,
                                    key_id=currentKey, created_at=datetime.now())
        file = EncryptedFileCRUD.create_file(db, file_dto)

        print(f"File encrypted successfully: {encrypted_file_path}")
        return True, "File encrypted successfully", file

    except subprocess.CalledProcessError as e:
        print(f"Error during encryption: {e}")
        if os.path.exists("keys/tempAESKey.txt"):
            os.remove("keys/tempAESKey.txt")
        return False, "Error during encryption", None


def encryptAES(file_path, db, currentKey):
    encrypted_file_path = (file_path + ".encrypted")

    command = [
        "openssl", "enc", "-aes-256-cbc",
        "-in", file_path,
        "-out", encrypted_file_path,
        "-kfile", "keys/keyfile.txt"
    ]

    process = subprocess.run(command, check=True, text=True, capture_output=True)
    if process.returncode == 0:

        hash = hashing.hash_file(file_path)

        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".encrypted", "")

        file_dto = EncryptedFileDTO(file_name=file_name, encrypted_path=encrypted_file_path, hash=hash, algorithm_id=1,
                                    key_id=currentKey, created_at=datetime.now())
        file = EncryptedFileCRUD.create_file(db, file_dto)

        print(f"File encrypted successfully: {encrypted_file_path}")
        return True, "File encrypted successfully", file
    else:
        print(f"Error during encryption")
        return False, "Error during encryption", None