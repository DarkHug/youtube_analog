from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func

from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    token_hash = Column(String, nullable=False, index=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    revoked = Column(Boolean, default=False, nullable=False)
