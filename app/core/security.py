import hashlib
import secrets

import bcrypt


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
