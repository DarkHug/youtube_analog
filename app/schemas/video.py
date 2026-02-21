import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.video import VideoStatus


class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class VideoRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime.datetime
    views: int
    likes_count: int
    is_liked: bool
    model_config = ConfigDict(from_attributes=True)


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class VideoListResponse(BaseModel):
    items: list[VideoRead]
    total: int
    limit: int
    offset: int


class UpdateVideoStatus(BaseModel):
    status: VideoStatus
