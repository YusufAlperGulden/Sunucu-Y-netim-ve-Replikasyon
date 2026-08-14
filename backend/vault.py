import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_encryption_key() -> bytes:
    """
    Derives an AES-256 bit key (url-safe base64) from the secret vault key.
    If VAULT_KEY is not set, a temporary one is created (NOT recommended for production).
    """
    secret = os.environ.get('VAULT_KEY', 'default-unsafe-dev-vault-key-1234')
    salt = b'universal-server-mgr-salt'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    return key

def encrypt(plaintext: str) -> str:
    """Encrypts a plaintext string into a safe token."""
    if not plaintext:
        return plaintext
    key = get_encryption_key()
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()

def decrypt(token: str) -> str:
    """Decrypts a token back to plaintext."""
    if not token:
        return token
    key = get_encryption_key()
    f = Fernet(key)
    try:
        return f.decrypt(token.encode()).decode()
    except Exception:
        raise ValueError("Failed to decrypt the token. The vault key might be incorrect.")
