import app.crud.channel as channel_crud


async def get_my_channel(session, user_id):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    return channel
