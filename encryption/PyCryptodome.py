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
import hashing.hash as hashing
import time
import tracemalloc


def encryptRSA(file_path, db, currentKey):
    start_time = time.perf_counter()
    encrypted_file_path = (file_path + ".encrypted")

    input_file = open(file_path, "rb")
    output_file = open(encrypted_file_path, "wb")

    pub = open("keys/public.pem", "r")
    pubKey = RSA.importKey(pub.read())
    pub.close()

    priv = open("keys/key.pem", "r")
    keyPair = RSA.importKey(priv.read())
    priv.close()

    aes_key = get_random_bytes(32)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)

    with open(file_path, "rb") as input_file, open(encrypted_file_path, "wb") as output_file:
        nonce = cipher_aes.nonce
        output_file.write(nonce)

        while chunk := input_file.read(64 * 1024):
            ciphertext = cipher_aes.encrypt(chunk)
            output_file.write(ciphertext)

        tag = cipher_aes.digest()
        output_file.write(tag)

        hash = hashing.hash_file(file_path)

        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".encrypted", "")

        with open("keys/public.pem", "rb") as key_file:
            rsa_key = RSA.import_key(key_file.read())
            cipher_rsa = PKCS1_OAEP.new(rsa_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)

        with open(encrypted_file_path + ".key", "wb") as key_out:
            key_out.write(encrypted_aes_key)

        end_time = time.perf_counter()
        print("*****", (end_time - start_time) * 1000)
        start_time = time.perf_counter()

        file_dto = EncryptedFileDTO(file_name=file_name, encrypted_path=encrypted_file_path, hash=hash, algorithm_id=0, key_id=currentKey, created_at=datetime.now())
        file = EncryptedFileCRUD.create_file(db, file_dto)
        end_time = time.perf_counter()
        print("*****", (end_time - start_time) * 1000)
        return True, "Successfully encrypted the file", file

def encryptAES(file_path, db, currentKey):
    encrypted_file_path = (file_path + ".encrypted")

    input_file = open(file_path, "rb")
    output_file = open(encrypted_file_path, "wb")

    with open("keys/keyfile.txt", "r") as key_file:
        key = bytes.fromhex(key_file.read())

    with open(file_path, "rb") as input_file, open(encrypted_file_path, "wb") as output_file:
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        output_file.write(nonce)

        while chunk := input_file.read(64 * 1024):
            ciphertext = cipher.encrypt(chunk)
            output_file.write(ciphertext)

        tag = cipher.digest()
        output_file.write(tag)

        hash = hashing.hash_file(file_path)

        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".encrypted", "")

        file_dto = EncryptedFileDTO(file_name=file_name, encrypted_path=encrypted_file_path, hash=hash, algorithm_id=1, key_id=currentKey, created_at=datetime.now())
        file = EncryptedFileCRUD.create_file(db, file_dto)

    return True, "Successfully encrypted the file", file