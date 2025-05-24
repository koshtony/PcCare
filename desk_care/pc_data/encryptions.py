import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def create_key_from_password(salt,password): 
    
    kdf =  PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    
UPLOAD_FOLDER = "ENCRYPTED_FILES"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def encrypt_file_password_method(file,password):
    
    salt = os.urandom(20) 
    key = create_key_from_password(salt,password)
    
    fernet = Fernet(key)
    
    file_info = file.read()
    
    encrypt_ = fernet.encrypt(file_info)
    
    save_as = file.filename + ".enc"
    
    save_as_path = os.path.join(UPLOAD_FOLDER,save_as)
    
    with open(save_as_path,"wb") as file: 
        
        file.write(salt + encrypt_)
        
    return f">Encrypted {save_as} Successfully"
        
        
def decrypt_file_password_method(filename,password): 
    
    with open(filename,"rb") as file:
        
        file_info = file.read() 
        
    salt = file_info[:20]
    encrypted_info = file_info[20:]
    
    key = create_key_from_password(salt,password)
    
    fernet = Fernet(key)
    
    decrypt_ = fernet.decrypt(encrypted_info)
    
    with open(filename,"wb") as file: 
        file.write(decrypt_)
