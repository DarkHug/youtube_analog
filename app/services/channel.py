import app.crud.channel as channel_crud


async def get_my_channel(session, user_id):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    return channel


async def update_channel(session, user_id, channel_data):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None

    await channel_crud.update_channel(session, channel, channel_data)
    session.commit()

    return channel
