# crud/user.py
from fastapi import HTTPException
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


async def login(session: AsyncSession, user_in: UserLogin):
    user = await get_user_by_email(session, user_in.email)
    if not user:
        return None

    if not verify_password(user_in.password, user.hashed_password):
        return None

    return create_access_token(user_id=user.id)

