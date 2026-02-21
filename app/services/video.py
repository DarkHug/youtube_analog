import app.crud.channel as channel_crud
import app.crud.video as video_crud
import app.crud.video_like as video_like_crud
from app.models.video import VideoStatus


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
    items, total = await video_crud.get_videos_by_channel(session, channel.id, limit, offset)
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }


async def get_video_by_id(session, video_id, user):
    result = await video_crud.get_video_with_meta(
        session,
        video_id,
        user.id if user else None,
    )

    if not result:
        return None

    video, likes_count, is_liked = result

    if video.status != VideoStatus.PUBLISHED:
        if not user:
            return None

        channel = await channel_crud.get_by_user_id(session, user.id)
        if not channel or video.channel_id != channel.id:
            return None

    if video.status == VideoStatus.PUBLISHED:
        await video_crud.increment_views(session, video_id)
        await session.commit()
        video.views += 1

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "created_at": video.created_at,
        "views": video.views,
        "likes_count": likes_count,
        "is_liked": is_liked,
    }


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


async def publish_video(session, video_id, user_id):
    video = await video_crud.get_video_by_id(session, video_id)
    if not video:
        return None
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    if video.channel_id != channel.id:
        return None
    if video.status != VideoStatus.PUBLISHED:
        video.status = VideoStatus.PUBLISHED
        await session.commit()
        await session.refresh(video)

    return video


async def change_video_status(session, video_id, user_id, target_status):
    video = await video_crud.get_video_by_id(session, video_id)
    if not video:
        return None
    channel = await channel_crud.get_by_user_id(session, user_id)
    if not channel:
        return None
    if video.channel_id != channel.id:
        return None
    if video.status == target_status:
        return video

    video.status = target_status

    await session.commit()
    await session.refresh(video)

    return video
