import os
from cryptography.fernet import Fernet

# Yüksek güvenlikli master key. Gerçek üretim ortamında çevre değişkeni (ENV) olarak alınmalı.
MASTER_KEY = b'G48B_U8D5t-9y4T3S1L0O2x-9w6a1-J9dK_8l2f6u1w='
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
