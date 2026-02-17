from sqlalchemy import select, func

from app.models.video import Video


async def create_video(session, channel_id, title, description):
    video = Video(channel_id=channel_id, title=title, description=description)
    session.add(video)
    return video


async def get_video_by_id(session, video_id, limit: int, offset: int):
    return await session.get(Video, video_id)


async def get_videos_by_channel(session, channel_id, limit: int, offset: int):
    stmt = select(Video).where(Video.channel_id == channel_id).order_by(Video.created_at.desc())
    count = select(func.count()).select_from(Video).where(Video.channel_id == channel_id)
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)
    videos = await session.execute(stmt)
    total = await session.scalar(count)

    items = videos.scalars().all()

    return items, total


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
