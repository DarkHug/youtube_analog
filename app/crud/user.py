# crud/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.core.verify import get_user_by_email
from app.schemas.user import UserCreate, UserLogin


async def create_user(session, user_in: UserCreate):
    email_check = await get_user_by_email(session, user_in.email)
    if email_check:
        return None

    hashed_password = hash_password(user_in.password)

    user = models.User(email=user_in.email, hashed_password=hashed_password)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def login(session, email: str, password: str) -> str | None:
    user = await get_user_by_email(session, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return create_access_token(user_id=user.id)


async def get_user_by_id(session, user_id: int):
    result = await session.scalar(
        select(models.User).where(models.User.id == user_id)
    )
    return result
