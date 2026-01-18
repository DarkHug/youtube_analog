import app.crud.user as user_crud
from app import models
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.crud.refresh_token import get_refresh_token, revoke_refresh_token, create_refresh_token
from app.schemas.user import UserCreate


async def register_user(session, user_in: UserCreate):
    email_check = await user_crud.get_user_by_email(session, user_in.email)
    if email_check:
        return None

    hashed_password = hash_password(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed_password)
    session.add(user)
    await session.flush()

    # логика создания канал

    await session.commit()
    await session.refresh(user)

    return user


async def login(session, email: str, password: str) -> str | None:
    user = await user_crud.get_user_by_email(session, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return create_access_token(user_id=user.id)


async def authenticate_user(session, email: str, password: str):
    user = await user_crud.get_user_by_email(session, email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def refresh_tokens(session, refresh_token: str):
    refresh_token_obj = await get_refresh_token(session, refresh_token)
    if refresh_token_obj is None:
        return None

    if refresh_token_obj.revoked:
        return None

    user_id = refresh_token_obj.user_id

    await revoke_refresh_token(refresh_token_obj)

    new_refresh_token = await create_refresh_token(session, user_id)
    new_access_token = create_access_token(user_id)

    await session.commit()
    return new_access_token, new_refresh_token


async def logout_user(session, refresh_token: str):
    result = await get_refresh_token(session, refresh_token)
    if result:
        await revoke_refresh_token(result)
        await session.commit()
    return None
