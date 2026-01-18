from app import models


async def create_channel(session, user_id, name, description):
    channel = models.Channel(user_id=user_id, name=name, description=description)
    session.add(channel)
