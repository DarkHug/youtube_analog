from app import models
from sqlalchemy import select


async def create_channel(session, user_id, name, description):
    channel = models.Channel(user_id=user_id, name=name, description=description)
    session.add(channel)


async def update_channel_fields(session, channel, data):
    if data.name is not None:
        channel.name = data.name
        session.add(channel)
    if data.description is not None:
        channel.description = data.description
        session.add(channel)


async def get_by_user_id(session, user_id) -> models.Channel | None:
    stmt = select(models.Channel).where(models.Channel.user_id == user_id)
    return await session.scalar(stmt)


async def get_by_id(session, channel_id):
    stmt = select(models.Channel).where(models.Channel.id == channel_id)
    return await session.scalar(stmt)
