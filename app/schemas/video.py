import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class VideoRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
