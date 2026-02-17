import app.crud.channel as channel_crud
import app.crud.video as video_crud


async def get_my_channel(session, user_id):
    channel = await channel_crud.get_by_user_id(session, user_id)
    return channel


async def update_my_channel(session, user_id, channel_data):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None

    await channel_crud.update_channel_fields(session, channel, channel_data)
    await session.commit()

    return channel


async def get_channel_by_id(session, channel_id):
    return await channel_crud.get_by_id(session, channel_id)


async def get_channel_videos(session, channel_id, limit, offset):
    channel = await channel_crud.get_by_id(session, channel_id)
    if not channel:
        return None
    items, total = await video_crud.get_videos_by_channel(session, channel.id, limit, offset)
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }
