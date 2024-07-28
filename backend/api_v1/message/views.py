from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.models import db_helper, Message
from . import crud

from .schemas import MessageSchema, MessageCreate, MessageResponse
from api_v1.jwt_auth.jwt_auth import get_current_token_payload


router = APIRouter(tags=["Messages"])


@router.get("/{chat_id}/{before_date}/{amount}/", response_model=list[MessageSchema])
async def get_messages(
    chat_id: Annotated[int, Path],
    before_date: Annotated[str, Path],
    amount: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
):
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    return await crud.get_messages(
        session=session,
        username=username,
        chat_id=chat_id,
        before_date=before_date,
        amount=amount,
    )


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    message_in: MessageCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
):
    creator_username: str | None = payload.get("sub")
    if not creator_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    return await crud.create_message(
        session=session, message_in=message_in, creator_username=creator_username
    )
