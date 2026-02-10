from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.deps.deps import get_current_user
from app.db.session import get_db
import app.schemas.video as video_schemas
import app.services.video as video_service
import app.crud.channel as channel_crud

router = APIRouter(
    prefix="/v1/video",
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


@router.get('/my', response_model=list[video_schemas.VideoRead], status_code=status.HTTP_200_OK)
async def my_videos(
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
):
    result = await video_service.get_my_videos(db, user.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result


@router.get('/{video_id}', response_model=video_schemas.VideoRead, status_code=status.HTTP_200_OK)
async def get_video_by_id(video_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    video = await video_service.get_video_by_id(db, video_id)
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
