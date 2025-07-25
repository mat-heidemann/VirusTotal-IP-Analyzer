"""
API key encryption and decryption utilities
"""
import os
from cryptography.fernet import Fernet
from .config import FERNET_KEY_FILE, API_KEY_FILE


class EncryptionManager:
    """Handles encryption and decryption of API keys"""
    
    def __init__(self):
        self.fernet = self._load_or_create_fernet()
    
    def _load_or_create_fernet(self):
        """Load existing Fernet key or create a new one"""
        if os.path.exists(FERNET_KEY_FILE):
            with open(FERNET_KEY_FILE, "rb") as f:
                return Fernet(f.read())
        else:
            key = Fernet.generate_key()
            with open(FERNET_KEY_FILE, "wb") as f:
                f.write(key)
            return Fernet(key)
    
    def encrypt_api_key(self, api_key: str) -> bytes:
        """Encrypt an API key"""
        return self.fernet.encrypt(api_key.encode())
    
    def decrypt_api_key(self, encrypted_key: bytes) -> str:
        """Decrypt an API key"""
        return self.fernet.decrypt(encrypted_key).decode()
    
    def save_api_key(self, api_key: str) -> None:
        """Save encrypted API key to file"""
        encrypted_key = self.encrypt_api_key(api_key)
        with open(API_KEY_FILE, "wb") as f:
            f.write(encrypted_key)
    
    def load_api_key(self) -> str:
        """Load and decrypt API key from file"""
        if not self.is_api_key_defined():
            raise FileNotFoundError("API key file not found")
        
        with open(API_KEY_FILE, "rb") as f:
            encrypted_key = f.read()
        
        return self.decrypt_api_key(encrypted_key)
    
    def is_api_key_defined(self) -> bool:
        """Check if API key file exists"""
        return os.path.exists(API_KEY_FILE)
