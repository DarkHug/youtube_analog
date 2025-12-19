from app import models
from sqlalchemy import select


async def get_user_by_email(session, email):
    query = select(models.User).where(models.User.email == email)
    result = await session.scalar(query)
    return result
