from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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
async def create_user(user: user_schemas.UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await crud.create_user(db, user)

    if res is None:
        raise HTTPException(status_code=400)

    return res


@router.post("/login", response_model=token_schemas.Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
):
    token = await crud.login(
        db,
        email=form_data.username,
        password=form_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=user_schemas.UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user
