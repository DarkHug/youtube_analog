from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = 'users'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, index=True)
    hashed_password = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    channel = relationship(
        "Channel",
        back_populates="user",
        uselist=False
    )

    video_likes = relationship(
        "VideoLike",
        back_populates="user",
    )
