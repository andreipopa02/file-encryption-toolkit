from database.dto.algorithm_dto import AlgorithmDTO
from database.dto.key_dto import KeyDTO
from database.dto.encrypted_file_dto import EncryptedFileDTO
from database.dto.performance_log_dto import PerformanceLogDTO
from database.crud.algorithm_crud import AlgorithmCRUD
from database.crud.key_crud import KeyCRUD
from database.crud.encrypted_file_crud import EncryptedFileCRUD
from database.crud.performance_log_crud import PerformanceLogCRUD
from database.database import SessionLocal, get_db
from performances.performance import caclculate_performances

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QTextEdit
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
from datetime import datetime
import subprocess
import encryption.OpenSSL as OpenSSLEncryption
import encryption.PyCryptodome as PyCryptodomeEncryption

import decryption.OpenSSL as OpenSSLDecryption
import decryption.PyCryptodome as PyCryptodomeDecryption

import key_generation.PyCryptodome as PyCryptodomeKeys
import key_generation.OpenSSL as OpenSSLKeys


class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.db = SessionLocal()

        self.currentKey = -1

    def init_ui(self):
        self.setWindowTitle("Encryption Key Management")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        self.file_button = QPushButton("Select File")
        self.file_button.clicked.connect(self.select_file)

        self.framework_label = QLabel("Select Framework:")
        self.framework_combo = QComboBox()
        self.framework_combo.addItems(["OpenSSL", "PyCryptodome"])

        self.algorithm_label = QLabel("Select Algorithm:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["AES", "RSA"])

        self.generate_key_button = QPushButton("Generate Key")
        self.generate_key_button.clicked.connect(self.generate_key)

        self.encrypt_button = QPushButton("Encrypt File")
        self.decrypt_button = QPushButton("Decrypt File")

        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.decrypt_button.clicked.connect(self.decrypt_file)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Output")

        layout.addWidget(self.file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.framework_label)
        layout.addWidget(self.framework_combo)
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.generate_key_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

        self.encrypt_button.setEnabled(False)
    
    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            self.file_label.setText(f"Selected: {file_path}")
            self.selected_file = file_path

    def generate_key(self):
        framework = self.framework_combo.currentText()
        algorithm = self.algorithm_combo.currentText()
        print(f"Generating key for {algorithm} using {framework}...")
        if framework == "OpenSSL":
            if algorithm == "AES":
                key_id, key = OpenSSLKeys.generateKeyAES(self.db)
                if key_id and key:
                    self.output_box.append(f'[{datetime.now()}] AES Key: \n{key}\n')
                    self.currentKey = key_id 
                    self.encrypt_button.setEnabled(True)

            else:
                key_id, key = OpenSSLKeys.generateKeyRSA(self.db)
                if key_id and key:
                    self.output_box.append(f'[{datetime.now()}] RSA Key: \n{key}\n')
                    self.currentKey = key_id
                    self.encrypt_button.setEnabled(True) 
                    
        elif framework == "PyCryptodome":
            if algorithm == "RSA":
                key_id, key = PyCryptodomeKeys.generateKeyRSA(self.db)
                self.output_box.append(f'[{datetime.now()}] RSA Key: \n{key}\n')
                self.currentKey = key_id 
                self.encrypt_button.setEnabled(True)

            elif algorithm == "AES":
                key_id, key = PyCryptodomeKeys.generateKeyAES(self.db)
                self.output_box.append(f'[{datetime.now()}] AES Key: \n{key}\n')
                self.currentKey = key_id
                self.encrypt_button.setEnabled(True) 

        else:
            print("No framework like that!")

    def encrypt_file(self):
        if hasattr(self, 'selected_file'):
            algorithm = self.algorithm_combo.currentText()
            framework = self.framework_combo.currentText()

            if self.currentKey == -1:
                self.output_box.append("You need to generate a key first!\n")
                return

            file_name = os.path.basename(self.selected_file)
            existingFile = EncryptedFileCRUD.get_file_by_name(self.db, file_name)
            if existingFile:
                self.output_box.append(
                    f'[{datetime.now()}] An encrypted file with the same name already exist. Please use a different name!\n')
                return

            print(f"Encrypting {self.selected_file} using {algorithm}...")
            encrypted_file_name = file_name + ".encrypted"
            if framework == "PyCryptodome":
                if algorithm == "RSA":
                    print(self.selected_file, self.db, self.currentKey)
                    success, msg = caclculate_performances(PyCryptodomeEncryption.encryptRSA, 'encryption',self.db,
                                                           self.currentKey,self.selected_file, self.db, self.currentKey)
                    if success:
                        self.output_box.append(
                            f'[{datetime.now()}] Successfully encrypted the file using RSA to {encrypted_file_name}\n')
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to encrypt the file: {msg}\n')
                elif algorithm == "AES":
                    success, msg = caclculate_performances(PyCryptodomeEncryption.encryptAES, 'encryption', self.db,
                                                           self.currentKey,self.selected_file, self.db, self.currentKey)
                    if success:
                        self.output_box.append(
                            f'[{datetime.now()}] Successfully encrypted the file using AES to {encrypted_file_name}\n')
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to encrypt the file: {msg}\n')

            elif framework == "OpenSSL":
                if algorithm == "RSA":
                    success, msg = caclculate_performances(OpenSSLEncryption.encryptRSA, 'encryption',self.db,
                                                           self.currentKey,self.selected_file, self.db, self.currentKey)
                    if success:
                        self.output_box.append(
                            f'[{datetime.now()}] Successfully encrypted the file using RSA to {encrypted_file_name}\n')
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to encrypt the file: {msg}\n')
                elif algorithm == "AES":
                    success, msg = caclculate_performances(OpenSSLEncryption.encryptAES, 'encryption',self.db,
                                                           self.currentKey,self.selected_file, self.db, self.currentKey)
                    if success:
                        self.output_box.append(
                            f'[{datetime.now()}] Successfully encrypted the file using AES to {encrypted_file_name}\n')
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to encrypt the file: {msg}\n')

    def decrypt_file(self):
        if hasattr(self, 'selected_file'):
            print(f"Decrypting {self.selected_file}...")
            file_name = os.path.basename(self.selected_file)

            if not file_name.endswith(".encrypted"):
                self.output_box.append(f'[{datetime.now()}] You can only decrypt files ending with ".encrypted"\n')
                return

            file_name = file_name.replace(".encrypted", "")
            file = EncryptedFileCRUD.get_file_by_name(self.db, file_name)

            if not file:
                self.output_box.append(f'[{datetime.now()}] There is no file with that name encrypted!\n')
                return

            keyInstance = KeyCRUD.get_key(self.db, file.key_id)

            #print(file.id)
            if keyInstance.key_framework == "PyCryptodome":
                if file.algorithm_id == 0:
                    success, msg = caclculate_performances(PyCryptodomeDecryption.decryptRSA, 'decryption',
                                                           self.db, keyInstance.id, file, keyInstance)
                    if success:
                        self.output_box.append(f'[{datetime.now()}] Successfully decrypted the file using RSA to {file_name}\n')
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to decrypt the file: {msg}\n')        
                    
                elif file.algorithm_id == 1:
                    success, msg = caclculate_performances(PyCryptodomeDecryption.decryptAES, 'decryption',
                                                           self.db, keyInstance.id, file, keyInstance)
                    if success:
                        self.output_box.append(f'[{datetime.now()}] Successfully decrypted the file using AES to {file_name}\n')   
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to decrypt the file: {msg}\n')     
                            
            elif keyInstance.key_framework == "OpenSSL":
                if file.algorithm_id == 0:
                    success, msg = caclculate_performances(OpenSSLDecryption.decryptRSA,  'decryption',
                                                           self.db, keyInstance.id, file, keyInstance)
                    if success:
                        self.output_box.append(f'[{datetime.now()}] Successfully decrypted the file using RSA to {file_name}\n')  
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to decrypt the file: {msg}\n')      
                    
                elif file.algorithm_id == 1:
                    success, msg = caclculate_performances(OpenSSLDecryption.decryptAES,  'decryption',
                                                           self.db, keyInstance.id, file, keyInstance)
                    if success:
                        self.output_box.append(f'[{datetime.now()}] Successfully decrypted the file using AES to {file_name}\n')  
                    else:
                        self.output_box.append(f'[{datetime.now()}] Failed to decrypt the file: {msg}\n')     

            print(f"File decrypted and saved to: {file.file_name}")
