from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.models import db_helper
from . import crud

from .schemas import ChatResponse, ChatCreate
from api_v1.jwt_auth.jwt_auth import get_current_token_payload


router = APIRouter(tags=["Chats"])


@router.get("/", response_model=list[ChatResponse])
async def get_chats(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
):
    username: str | None = payload.get("sub")
    return await crud.get_chats(session=session, username=username)


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat(
    chat_in: ChatCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
):
    creator_username: str | None = payload.get("sub")
    if not creator_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    return await crud.create_chat(
        session=session, chat_in=chat_in, creator_username=creator_username
    )
    # pass
