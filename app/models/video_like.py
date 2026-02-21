from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class VideoLike(Base):
    __tablename__ = 'video_likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='video_likes')
    video = relationship('Video', back_populates='video_likes')

    __table_args__ = (
        UniqueConstraint('video_id', 'user_id', name='uniq_video_likes'),
    )
