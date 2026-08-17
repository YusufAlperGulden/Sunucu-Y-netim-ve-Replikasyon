import os
from cryptography.fernet import Fernet

# Yüksek güvenlikli master key çevresel değişkenden alınır.
_env_key = os.environ.get('VAULT_KEY')
if _env_key:
    MASTER_KEY = _env_key.encode()
else:
    # Güvenli değil ama fallback olarak rastgele key. Restart'ta veriler gider, uyarıdır.
    print("WARNING: VAULT_KEY not found in environment, using random key.")
    MASTER_KEY = Fernet.generate_key()

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
        return "Decryption Error"
