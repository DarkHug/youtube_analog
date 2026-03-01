import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum, BigInteger
from sqlalchemy.orm import relationship

from app.db.base import Base


class VideoStatus(enum.StrEnum):
    DRAFT = 'draft'
    PUBLISHED = 'published'


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(
        Enum(
            VideoStatus,
            name="video_status",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
        server_default="draft",
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False, index=True)
    channel = relationship('Channel', back_populates='videos')
    views = Column(Integer, nullable=False, server_default="0")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    video_likes = relationship('VideoLike', back_populates='video')
