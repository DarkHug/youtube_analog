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
    base_stmt = select(Video).where(Video.channel_id == channel_id).order_by(Video.created_at.desc())
    if only_published:
        base_stmt = base_stmt.where(Video.status == VideoStatus.PUBLISHED)
    base_count = select(func.count()).select_from(Video).where(Video.channel_id == channel_id)
    if only_published:
        base_count = base_count.where(Video.status == VideoStatus.PUBLISHED)
    if limit is not None:
        base_stmt = base_stmt.limit(limit)
    if offset is not None:
        base_stmt = base_stmt.offset(offset)
    videos = await session.execute(base_stmt)
    total = await session.scalar(base_count)

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


async def increment_views(session, video_id):
    video = update(Video).where(Video.id == video_id).values(views=Video.views + 1)
    await session.execute(video)


async def get_video_with_meta(session, video_id: int, user_id: int | None):
    if user_id is not None:
        is_liked_expr = (
            exists()
            .where(
                VideoLike.video_id == Video.id,
                VideoLike.user_id == user_id,
            )
            .correlate(Video)
            .label("is_liked")
        )
    else:
        is_liked_expr = literal(False).label("is_liked")

    stmt = (
        select(
            Video,
            func.count(VideoLike.id).label("likes_count"),
            is_liked_expr,
        )
        .outerjoin(VideoLike, VideoLike.video_id == Video.id)
        .where(Video.id == video_id)
        .group_by(Video.id)
    )

    result = await session.execute(stmt)
    row = result.first()

    if not row:
        return None

    video, likes_count, is_liked = row
    return video, likes_count, is_liked
