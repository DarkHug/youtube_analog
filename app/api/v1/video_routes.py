from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.deps.deps import get_current_user
from app.db.session import get_db
import app.schemas.video as video_schema
import app.services.video as video_service
import app.crud.channel as channel_crud

router = APIRouter(
    prefix="/v1/video",
    tags=["Video"],
)


@router.post("/create", response_model=video_schema.VideoRead, status_code=status.HTTP_201_CREATED)
async def create_video(
        video_data: video_schema.VideoCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
):
    video = await video_service.create_video(db, user.id, video_data)
    if video is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return video


@router.get('/my', response_model=list[video_schema.VideoRead], status_code=status.HTTP_200_OK)
async def my_videos(
        db: Annotated[AsyncSession, Depends(get_db)],
        user=Depends(get_current_user),
):
    result = await video_service.get_my_videos(db, user.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result
