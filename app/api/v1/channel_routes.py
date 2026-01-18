from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.deps.deps import get_current_user
from app.db.session import get_db
import app.services.channel as channel_service

router = APIRouter(
    prefix="/v1/channel",
    tags=["Channel"],
)


@router.get("/me")
async def my_channel(
        user=Depends(get_current_user),
        db=Depends(get_db)
):
    channel = await channel_service.get_my_channel(db, user.id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return channel
