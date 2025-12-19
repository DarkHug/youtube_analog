from datetime import datetime, timedelta
from jose import jwt, JWTError

secret_key = "chatgpt+almas=best_team"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = timedelta(minutes=30)


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE_TIME,
    }
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Token payload missing sub")
        return int(user_id)
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e
