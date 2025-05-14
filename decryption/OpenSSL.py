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

import hashing.hash as hashing

def decryptRSA(file, keyInstance):
    private_key_pem = keyInstance.private_key

    with open("keys/key.pem", "w") as key_file:
        key_file.write(private_key_pem)

    encrypted_key_file = file.encrypted_path + ".key"
    
    try:
        # Decrypt the AES Key using RSA
        subprocess.run([
            "openssl", "pkeyutl", "-decrypt",
            "-inkey", "keys/key.pem",
            "-in", encrypted_key_file, "-out", (encrypted_key_file + ".decrypted")
        ], check=True)

        # Decrypt the file using AES
        subprocess.run([
            "openssl", "enc", "-d", "-aes-256-cbc",
            "-in", file.encrypted_path,
            "-out", file.file_name,
            "-kfile", (encrypted_key_file + ".decrypted")
        ], check=True)

        os.remove(encrypted_key_file + ".decrypted")

        print("Original Hash:\n" +  file.hash)

        decrypted_hash = hashing.hash_file(file.file_name)

        print("Decrypted Hash:\n" + decrypted_hash)

        if decrypted_hash != file.hash:
            print("The decrypted file's hash doesn't match the original file's hash!")
            os.remove(file.file_name)
            return False, "The decrypted file's hash doesn't match the original file's hash!"
        
        return True, "Successfully decrypted the file", file

    except subprocess.CalledProcessError as e:
        print(f"Error during decryption: {e}")
        if os.path.exists(encrypted_key_file + ".decrypted"):
            os.remove(encrypted_key_file + ".decrypted")
        return False, "Error during decryption", file

def decryptAES(file, encryptedFile, keyInstance):
    private_key = keyInstance.private_key

    with open("keys/keyfile.txt", "w") as key_file:
        key_file.write(private_key)

    command = [
        "openssl", "enc", "-d", "-aes-256-cbc", 
        "-in", encryptedFile,
        "-out", file.file_name,
        "-kfile", "keys/keyfile.txt"
    ]
    
    try:
        subprocess.run(command, check=True)

        decrypted_hash = hashing.hash_file(file.file_name)

        if decrypted_hash != file.hash:
            print("The decrypted file's hash doesn't match the original file's hash!")
            os.remove(file.file_name)
            return False, "The decrypted file's hash doesn't match the original file's hash!"
        
        return True, "Successfully decrypted the file", file

    except subprocess.CalledProcessError as e:
        print(f"Error during decryption: {e}")
        return False, "Error during decryption", file