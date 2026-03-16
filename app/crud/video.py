from sqlalchemy import select, func, update, exists, literal

from app.models import VideoLike
from app.models.video import Video, VideoStatus


async def create_video(session, channel_id, title, description):
    video = Video(channel_id=channel_id, title=title, description=description)
    session.add(video)
    return video


async def get_video_by_id(session, video_id):
    return await session.get(Video, video_id)


async def get_videos_by_channel(session, channel_id, limit: int, offset: int, only_published: bool = False):
    base_stmt = (
        select(Video, func.count(VideoLike.id).label("likes_count"))
        .outerjoin(VideoLike, VideoLike.video_id == Video.id)
        .where(Video.channel_id == channel_id)
        .group_by(Video.id)
        .order_by(Video.created_at.desc())
    )
    if only_published:
        base_stmt = base_stmt.where(Video.status == VideoStatus.PUBLISHED)

    base_count = select(func.count()).select_from(Video).where(Video.channel_id == channel_id)
    if only_published:
        base_count = base_count.where(Video.status == VideoStatus.PUBLISHED)
    if limit is not None:
        base_stmt = base_stmt.limit(limit)
    if offset is not None:
        base_stmt = base_stmt.offset(offset)

    result = await session.execute(base_stmt)
    total = await session.scalar(base_count)

    rows = result.all()
    return rows, total


async def is_video_liked_by_user(session, video_id: int, user_id: int) -> bool:
    stmt = select(
        exists().where(
            VideoLike.video_id == video_id,
            VideoLike.user_id == user_id,
        )
    )
    result = await session.scalar(stmt)
    return bool(result)


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


async def get_video_with_meta(session, video_id: int):
    stmt = (
        select(
            Video,
            func.count(VideoLike.id).label("likes_count"),
        )
        .outerjoin(VideoLike, VideoLike.video_id == Video.id)
        .where(Video.id == video_id)
        .group_by(Video.id)
    )

    result = await session.execute(stmt)
    row = result.first()

    if not row:
        return None

    video, likes_count = row
    return video, likes_count


async def get_views_by_id(session, video_id: int) -> int | None:
    stmt = select(Video.views).where(Video.id == video_id)
    return await session.scalar(stmt)
