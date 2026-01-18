# crud/user.py

from sqlalchemy import select

from app import models


async def get_user_by_email(session, email):
    query = select(models.User).where(models.User.email == email)
    result = await session.scalar(query)
    return result


async def get_user_by_id(session, user_id: int):
    result = await session.scalar(
        select(models.User).where(models.User.id == user_id)
    )
    return result
