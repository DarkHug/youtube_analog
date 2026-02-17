from sqlalchemy import select

from app.models.video import Video


async def create_video(session, channel_id, title, description):
    video = Video(channel_id=channel_id, title=title, description=description)
    session.add(video)
    return video


async def get_video_by_id(session, video_id):
    return await session.get(Video, video_id)


async def get_videos_by_channel(session, channel_id):
    stmt = select(Video).where(Video.channel_id == channel_id).order_by(Video.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_video(session, video, data):
    if data.title is not None:
        video.title = data.title
        session.add(video)
    if data.description is not None:
        video.description = data.description
        session.add(video)


async def delete_video(session, video):
    if video is not None:
        session.delete(video)
