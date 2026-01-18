from app import models
from sqlalchemy import select

async def create_channel(session, user_id, name, description):
    channel = models.Channel(user_id=user_id, name=name, description=description)
    session.add(channel)



async def get_by_user_id(session, user_id) -> models.Channel | None:
    stmt = select(models.Channel).where(models.Channel.user_id == user_id)
    return await session.scalar(stmt)
