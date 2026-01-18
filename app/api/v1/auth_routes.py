from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import app.services.auth as auth_service
import app.crud.user as crud
import app.schemas.token as token_schemas
import app.schemas.user as user_schemas
from app.api.deps.deps import get_current_user
from app.db.session import get_db

router = APIRouter(
    prefix="/v1",
    tags=["User Authentication"],
)


@router.post('/register', response_model=user_schemas.UserRead)
async def register_user(user: user_schemas.UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await auth_service.register_user(db, user)

    if res is None:
        raise HTTPException(status_code=400)

    return res


@router.post("/login", response_model=token_schemas.AccessTokenResponse)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
):
    user = await auth_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = auth_service.create_access_token(user.id)
    refresh_token = await auth_service.create_refresh_token(db, user.id)
    await db.commit()
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=user_schemas.UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=token_schemas.AccessTokenResponse)
async def refresh(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    result = await auth_service.refresh_tokens(db, token)

    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token, refresh_token = result

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await auth_service.logout_user(db, refresh_token)

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
