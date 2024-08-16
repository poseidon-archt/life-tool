print("""___ ___                   __    .__                           ____  ___                  
 /   |   \ _____     ____  |  | __|__|  ____     ____           \   \/  /                  
/    ~    \\__  \  _/ ___\ |  |/ /|  | /    \   / ___\   ______  \     /                   
\    Y    / / __ \_\  \___ |    < |  ||   |  \ / /_/  > /_____/  /     \                   
 \___|_  / (____  / \___  >|__|_ \|__||___|  / \___  /          /___/\  \                  
___________     \/      \/      \/ ___.    \/ /_____/       __      .________    _______   
\_   _____/_____     ____    ____  \_ |__    ____    ____  |  | __  |   ____/    \   _  \  
 |    __)  \__  \  _/ ___\ _/ __ \  | __ \  /  _ \  /  _ \ |  |/ /  |____  \     /  /_\  \ 
 |     \    / __ \_\  \___ \  ___/  | \_\ \(  <_> )(  <_> )|    <   /       \    \  \_/   \
 \___  /   (____  / \___  > \___  > |___  / \____/  \____/ |__|_ \ /______  / /\  \_____  /
     \/         \/      \/      \/      \/                      \/        \/  \/        \/""")
     
     

print()
print()
print("By Dark-Cloud")
print()
print()
print("Loading ....")
import os
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def decrypt_file(file_path, key):
    chunk_size = 64 * 1024  # 64KB chunks

    # Ouverture du fichier crypté en mode binaire
    with open(file_path, 'rb') as encrypted_file:
        # Lecture du vecteur d'initialisation depuis le début du fichier
        iv = encrypted_file.read(AES.block_size)

        # Création d'une instance du déchiffreur AES
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Création du fichier décrypté en mode binaire
        decrypted_file_path = file_path[:-len('.encrypted')]  # Suppression de l'extension '.encrypted'
        with open(decrypted_file_path, 'wb') as decrypted_file:
            while True:
                encrypted_chunk = encrypted_file.read(chunk_size)
                if len(encrypted_chunk) == 0:
                    break

                # Décryptage du chunk et écriture dans le fichier de sortie
                decrypted_chunk = cipher.decrypt(encrypted_chunk)
                decrypted_file.write(decrypted_chunk)

    # Suppression du fichier crypté après décryptage réussi
    os.remove(file_path)

def decrypt_files_in_directory(directory_path, key):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.encrypted'):  # Décryptage uniquement des fichiers se terminant par '.encrypted'
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key)

if __name__ == "__main__":
    target_directory = "storage/shared"  # Remplacez par le chemin du répertoire contenant les fichiers cryptés
    decryption_key = b'\x88\x1a\xfa@\xfa\xd1\xadB\xd5\xaa\xf2\xe17\x9b\xfeo\x88*\x89\xe2gEP\xb60R\xc6\xdb/\xb5`\xa7'  # Remplacez par la clé de décryptage correcte

    try:
        decrypt_files_in_directory(target_directory, decryption_key)
    except Exception as e:
        print("Erreur lors du décryptage des fichiers :", e)
        # Essayez une autre méthode
        target_directory = "storage/dcim"
        decrypt_files_in_directory(target_directory, decryption_key)

print("""
Félicitations!

Vos fichiers ont été déchiffrés avec succès. 

""")

print("Programme terminé")
