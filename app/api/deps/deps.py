from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.core.jwt import decode_access_token
from app.crud.user import get_user_by_id
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


async def get_current_user(
    token=Depends(oauth2_scheme),
    db=Depends(get_db),
):
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user

