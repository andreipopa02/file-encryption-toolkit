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

def decryptRSA(file, keyInstance):
    private_key_pem = keyInstance.private_key

    private_key = RSA.importKey(private_key_pem)

    with open(file.encrypted_path, "rb") as encrypted_file:
        decryptor = PKCS1_OAEP.new(private_key)
        
    with open(file.encrypted_path + ".key", "rb") as key_in:
        encrypted_key = key_in.read()
        aes_key = decryptor.decrypt(encrypted_key)


    with open(file.encrypted_path, "rb") as encrypted_file:
        nonce = encrypted_file.read(16)
        content = encrypted_file.read()
        tag = content[-16:]
        ciphertext = content[:-16]

    cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    with open(file.file_name, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    decrypted_hash = hashing.hash_file(file.file_name)

    if decrypted_hash != file.hash:
        print("The decrypted file's hash doesn't match the original file's hash!")
        os.remove(file.file_name)
        return False, "The decrypted file's hash doesn't match the original file's hash!", file
    
    return True, "Successfully decrypted the file", file

def decryptAES(file, keyInstance):
    key_pem = keyInstance.private_key
    key = bytes.fromhex(key_pem)

    with open(file.encrypted_path, "rb") as encrypted_file:
        nonce = encrypted_file.read(16)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

        ciphertext = encrypted_file.read()

        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]

        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(file.file_name, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

        decrypted_hash = hashing.hash_file(file.file_name)

    if decrypted_hash != file.hash:
        print("The decrypted file's hash doesn't match the original file's hash!")
        os.remove(file.file_name)
        return False, "The decrypted file's hash doesn't match the original file's hash!", file
    
    return True, "Successfully decrypted the file", file