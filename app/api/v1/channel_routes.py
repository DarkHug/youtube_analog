from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.deps.deps import get_current_user
from app.db.session import get_db
import app.services.channel as channel_service
import app.schemas.channel as channel_schema
from app.schemas.video import VideoListResponse

router = APIRouter(
    prefix="/v1/channel",
    tags=["Channel"],
)


@router.get("/me")
async def my_channel(
        user=Depends(get_current_user),
        db=Depends(get_db)
):
    channel = await channel_service.get_my_channel(db, user.id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return channel


@router.patch("/me", response_model=channel_schema.ChannelRead)
async def update_channel(
        channel_to_update: channel_schema.ChannelUpdate,
        user=Depends(get_current_user),
        db=Depends(get_db),
) -> channel_schema.ChannelRead:
    channel = await channel_service.update_my_channel(db, user, channel_to_update)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return channel


@router.get("/{channel_id}/videos", response_model=VideoListResponse)
async def get_channel_videos(
        db: Annotated[AsyncSession, Depends(get_db)],
        channel_id: int,
        limit: int = Query(default=10, le=100), offset: int = 0
):
    result = await channel_service.get_channel_videos(db, channel_id, limit, offset)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.get("/{channel_id}", response_model=channel_schema.ChannelRead)
async def get_channel_by_id(
        channel_id: int,
        db=Depends(get_db),
):
    channel = await channel_service.get_channel_by_id(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return channel
