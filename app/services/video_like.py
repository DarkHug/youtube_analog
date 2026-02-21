from sqlalchemy.exc import IntegrityError

import app.crud.video as video_crud
import app.crud.video_like as video_like_crud
from app.models.video import VideoStatus


async def like_video(session, user_id: int, video_id: int):
    video = await video_crud.get_video_by_id(session, video_id)

    if video is None or video.status != VideoStatus.PUBLISHED:
        return None

    try:
        await video_like_crud.like_video(session, user_id, video_id)
        await session.commit()
    except IntegrityError:
        await session.rollback()

    result = await video_crud.get_video_with_meta(session, video_id, user_id)
    if not result:
        return None

    video, likes_count, is_liked = result

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "created_at": video.created_at,
        "views": video.views,
        "likes_count": likes_count,
        "is_liked": is_liked,
    }


async def unlike_video(session, user_id: int, video_id: int):
    video = await video_crud.get_video_by_id(session, video_id)
    if video is None or video.status != VideoStatus.PUBLISHED:
        return None
    await video_like_crud.unlike_video(session, user_id, video_id)
    await session.commit()
    return True
