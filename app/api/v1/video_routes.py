from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import app.schemas.video as video_schemas
import app.services.video as video_service
from app.api.deps.deps import get_current_user, get_optional_user
from app.db.session import get_db

router = APIRouter(
    prefix="/v1/videos",
    tags=["Video"],
)


@router.post("/create", response_model=video_schemas.VideoRead, status_code=status.HTTP_201_CREATED)
async def create_video(
        video_data: video_schemas.VideoCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
):
    video = await video_service.create_video(db, user.id, video_data)
    if video is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return video


@router.get('/my', response_model=video_schemas.VideoListResponse, status_code=status.HTTP_200_OK)
async def my_videos(
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
        limit: int = Query(default=10, le=100), offset: int = 0
):
    result = await video_service.get_my_videos(db, user.id, limit, offset)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.get('/{video_id}', response_model=video_schemas.VideoRead, status_code=status.HTTP_200_OK)
async def get_video_by_id(video_id: int,
                          db: Annotated[AsyncSession, Depends(get_db)],
                          user=Depends(get_optional_user)):
    video = await video_service.get_video_by_id(db, video_id, user)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return video


@router.patch('/{video_id}', response_model=video_schemas.VideoRead, status_code=status.HTTP_200_OK)
async def update_video(video_id: int,
                       video_data: video_schemas.VideoUpdate,
                       db: Annotated[AsyncSession, Depends(get_db)],
                       user=Depends(get_current_user)):
    video = await video_service.update_video(db, video_id, user.id, video_data)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if video == "forbidden":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return video


@router.delete('/{video_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: int,
                       db: Annotated[AsyncSession, Depends(get_db)],
                       user=Depends(get_current_user),
                       ):
    video = await video_service.delete_video(db, video_id, user.id)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if video == "forbidden":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return None


@router.patch('/{video_id}/change_status', response_model=video_schemas.VideoRead, status_code=status.HTTP_200_OK)
async def change_video_status(
        video_id: int,
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
):
    video = await video_service.change_video_status(db, video_id, user.id)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return video
