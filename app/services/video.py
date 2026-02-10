import app.crud.channel as channel_crud
import app.crud.video as video_crud
from app.schemas.video import VideoCreate


async def create_video(session, user_id, video_data):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    video = await video_crud.create_video(session, channel.id, video_data.title, video_data.description)
    await session.commit()
    return video


async def get_my_videos(session, user_id):
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    return await video_crud.get_videos_by_channel(session, channel.id)


async def get_video_by_id(session, video_id):
    video = await video_crud.get_video_by_id(session, video_id)
    return video
