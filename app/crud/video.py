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
