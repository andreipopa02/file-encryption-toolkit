import hashlib

def hash_file(filepath):
        h = hashlib.sha256()

        with open(filepath,'rb') as file:

            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)

        return h.hexdigest()