from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ChannelRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChannelUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)
