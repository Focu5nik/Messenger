from datetime import datetime
from fastapi import HTTPException, status

from sqlalchemy import select, func, ScalarResult, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models import UserChatAssociation, Chat, Message, User
from auth import utils as auth_utils

from .schemas import MessageCreate


async def create_message(
    session: AsyncSession, message_in: MessageCreate, creator_username: str
) -> Message:
    stmt = (
        select(User)
        .options(selectinload(User.chats_details).joinedload(UserChatAssociation.chat))
        .where(User.username == creator_username)
    )

    user = (await session.scalars(stmt)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat or User not found!",
        )

    flag = False
    for chat_user_details in user.chats_details:
        if chat_user_details.chat.id == message_in.chat_id:
            flag = True

    if not flag:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not your chat",
        )

    message_data = message_in.model_dump()
    message_data["sender_user_id"] = user.id
    new_message = Message(**message_data)
    session.add(new_message)
    await session.commit()
    return new_message


async def get_messages(
    session: AsyncSession,
    username: str,
    chat_id: int,
    before_date: str,
    amount: int,
) -> list[Message]:

    stmt = (
        select(Chat)
        .options(selectinload(Chat.users_details).joinedload(UserChatAssociation.user))
        .where(Chat.id == chat_id)
    )
    chat = (await session.scalars(stmt)).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no such chat"
        )
    print(username)
    flag = False
    for chat_user_details in chat.users_details:
        print(chat_user_details.user.username)
        if chat_user_details.user.username == username:
            flag = True

    if not flag:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"not your chat"
        )
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    before_date = datetime.strptime(before_date, datetime_format)
    # example 2024-05-19T08:31:48.372Z
    stmt = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .filter(Message.created_at <= before_date)
        .order_by(desc(Message.created_at))
        .limit(amount)
    )

    messages: ScalarResult[Message] = await session.scalars(stmt)

    return list(messages)
