import os
from cryptography.fernet import Fernet

# Yüksek güvenlikli master key çevresel değişkenden alınır.
_env_key = os.environ.get('VAULT_KEY')
if not _env_key:
    raise ValueError("CRITICAL: VAULT_KEY environment variable is missing. It is required to encrypt and decrypt database credentials safely. Please set it before starting the application.")

MASTER_KEY = _env_key.encode()

f = Fernet(MASTER_KEY)

def encrypt(data: str) -> str:
    """Verilen metni (örn: DB şifresi) AES-256 ile şifreler."""
    if not data:
        return data
    return f.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    """Şifrelenmiş metni çözer."""
    if not token:
        return token
    try:
        return f.decrypt(token.encode()).decode()
    except Exception as e:
        return None
