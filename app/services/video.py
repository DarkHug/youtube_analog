import app.crud.channel as channel_crud
import app.crud.video as video_crud


async def create_video(session, user_id, video_data):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    video = await video_crud.create_video(session, channel.id, video_data.title, video_data.description)
    await session.commit()
    return video


async def get_my_videos(session, user_id, limit: int, offset: int):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    return await video_crud.get_videos_by_channel(session, channel.id, limit, offset)


async def get_video_by_id(session, video_id):
    video = await video_crud.get_video_by_id(session, video_id)
    return video


async def update_video(session, video_id, user_id, video_data):
    video = await video_crud.get_video_by_id(session, video_id)
    if not video:
        return None
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    if video.channel_id != channel.id:
        return 'forbidden'
    await video_crud.update_video(session, video, video_data)
    await session.commit()
    return video


async def delete_video(session, video_id, user_id):
    video = await video_crud.get_video_by_id(session, video_id)
    if not video:
        return None
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    if video.channel_id != channel.id:
        return 'forbidden'
    await video_crud.delete_video(session, video)
    await session.commit()
    return True
