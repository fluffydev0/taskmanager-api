import hashlib
import secrets


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}${digest.hex()}"


def password_matches(password: str, stored: str) -> bool:
    salt_hex, _digest = stored.split("$", 1)
    return secrets.compare_digest(hash_password(password, bytes.fromhex(salt_hex)), stored)


def new_token() -> str:
    return secrets.token_urlsafe(32)
