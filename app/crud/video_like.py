from sqlalchemy import delete, exists
from sqlalchemy import select, func

from app.models import VideoLike


async def like_video(session, user_id, video_id):
    stmt = VideoLike(video_id=video_id, user_id=user_id)
    session.add(stmt)


async def unlike_video(session, user_id, video_id):
    stmt = delete(VideoLike).where(VideoLike.video_id == video_id, VideoLike.user_id == user_id)
    await session.execute(stmt)


async def count_likes(session, video_id):
    stmt = (
        select(func.count())
        .select_from(VideoLike)
        .where(VideoLike.video_id == video_id)
    )
    return await session.scalar(stmt) or 0


async def is_liked(session, video_id: int, user_id: int) -> bool:
    stmt = select(
        exists().where(
            VideoLike.video_id == video_id,
            VideoLike.user_id == user_id,
        )
    )
    result = await session.scalar(stmt)
    return bool(result)
