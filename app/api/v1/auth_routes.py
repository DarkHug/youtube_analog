from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import app.schemas.user as user_schemas
import app.schemas.token as token_schemas
from app.core.jwt import create_access_token
from app.db.session import get_db

import app.crud.user as crud

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


@router.post('/login', response_model=token_schemas.Token)
async def login(user: user_schemas.UserLogin, db: Annotated[AsyncSession, Depends(get_db)]):
    token = await crud.login(db, user)
    if token is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return {
        "access_token": token,
        "token_type": "bearer",
    }
