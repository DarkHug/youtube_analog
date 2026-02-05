from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False, index=True)
    channel = relationship('Channel', back_populates='videos')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
