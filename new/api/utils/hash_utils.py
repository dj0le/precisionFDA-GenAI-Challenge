import hashlib

def get_file_hash(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()
