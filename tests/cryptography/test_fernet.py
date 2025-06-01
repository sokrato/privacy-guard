import base64
import hashlib
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def test_fernet_encryption_decryption():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    original_message = b"A secret message"
    encrypted_message = cipher_suite.encrypt(original_message)
    decrypted_message = cipher_suite.decrypt(encrypted_message)

    assert original_message == decrypted_message


def test_fernet_encryption_with_password():
    password = b"random password"
    salt = secrets.token_bytes(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.b64encode(kdf.derive(password))
    cipher_suite = Fernet(key)

    original_message = b"A secret message"
    encrypted_message = cipher_suite.encrypt(original_message)
    decrypted_message = cipher_suite.decrypt(encrypted_message)

    assert original_message == decrypted_message


def test_pbkdf2():
    password = b"random password"
    salt = secrets.token_bytes(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
    )
    key1 = kdf.derive(password)

    key2 = hashlib.pbkdf2_hmac("sha256", password, salt, 10000, 32)
    assert key1 == key2
