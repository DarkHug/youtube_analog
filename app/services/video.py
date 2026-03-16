import json

import app.crud.channel as channel_crud
import app.crud.video as video_crud
import app.services.cache_service as cache_service
import app.crud.video_like as video_like_crud
from app.models.video import VideoStatus
from app.infrastructure.rabbitmq import publish_message


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

    rows, total = await video_crud.get_videos_by_channel(session, channel.id, limit, offset)

    items = [
        {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "status": video.status,
            "views": video.views,
            "created_at": video.created_at,
            "likes_count": likes_count,
            "is_liked": False,
        }
        for video, likes_count in rows
    ]

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


async def increment_and_get_views(
        redis,
        session,
        video_id: int,
        fallback_db_views: int | None = None,
) -> int:
    views_key = f"video:{video_id}:views"

    current = await redis.get(views_key)

    if current is None:
        if fallback_db_views is not None:
            db_views = fallback_db_views
        else:
            db_views = await video_crud.get_views_by_id(session, video_id)
            if db_views is None:
                raise ValueError("Video not found")

        await redis.set(views_key, db_views)

    new_value = await redis.incr(views_key)
    return new_value


async def get_video_by_id(redis, session, video_id: int, user):
    meta_key = f"video:{video_id}:meta"

    cached_meta = await cache_service.get(redis, meta_key)

    if cached_meta:
        views = await increment_and_get_views(
            redis,
            session,
            video_id,
        )

        await publish_message(
            routing_key="video.views.sync",
            data={"video_id": video_id, "views": 1},
        )

        if user:
            is_liked = await video_like_crud.is_liked(
                session,
                video_id,
                user.id,
            )
        else:
            is_liked = False

        return {
            **cached_meta,
            "views": views,
            "is_liked": is_liked,
        }

    # 2️⃣ Cache MISS → идём в БД
    result = await video_crud.get_video_with_meta(session, video_id)
    if not result:
        return None

    video, likes_count = result

    # 3️⃣ Проверка доступа
    if video.status != VideoStatus.PUBLISHED:
        if not user:
            return None

        channel = await channel_crud.get_by_user_id(session, user.id)
        if not channel or video.channel_id != channel.id:
            return None

        # Draft не кешируем и не инкрементим views
        return {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "created_at": video.created_at,
            "views": video.views,
            "likes_count": likes_count,
            "is_liked": False,
        }

    # 4️⃣ Published → работаем с views через Redis
    views = await increment_and_get_views(
        redis,
        session,
        video_id,
        fallback_db_views=video.views,
    )

    await publish_message(
        routing_key="video.views.sync",
        data={"video_id": video_id, "views": 1},
    )

    # 5️⃣ Сохраняем meta в кеш (без views)
    to_cache = {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "created_at": video.created_at.isoformat(),
        "likes_count": likes_count,
    }

    await cache_service.set(redis, meta_key, to_cache, ttl=60)

    # 6️⃣ is_liked
    if user:
        is_liked = await video_like_crud.is_liked(
            session,
            video_id,
            user.id,
        )
    else:
        is_liked = False

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "created_at": video.created_at,
        "views": views,
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
