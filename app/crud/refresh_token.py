from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.security import generate_refresh_token, hash_refresh_token
from app.models.refresh_token import RefreshToken

refresh_token_lifetime = timedelta(days=15)


async def create_refresh_token(session, user_id) -> str:
    origin_token = generate_refresh_token()
    hashed_token = hash_refresh_token(origin_token)

    refresh_token_model = RefreshToken(user_id=user_id, token_hash=hashed_token,
                                       expires_at=datetime.utcnow() + refresh_token_lifetime, revoked=False)
    session.add(refresh_token_model)

    return origin_token


async def get_refresh_token(session, token: str):
    hashed_token = hash_refresh_token(token)

    qs = await session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hashed_token)
    )
    if not qs:
        return None

    if qs.revoked:
        return None

    if qs.expires_at < datetime.now(timezone.utc):
        return None

    return qs


async def revoke_refresh_token(refresh_token: RefreshToken):
    refresh_token.revoked = True
