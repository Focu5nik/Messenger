from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import UserChatAssociation, Chat, User
from auth import utils as auth_utils

from .schemas import ChatResponse, ChatCreate


async def create_chat(
    session: AsyncSession, chat_in: ChatCreate, creator_username: str
) -> ChatResponse:
    new_chat = Chat(name=chat_in.name, chat_picture=chat_in.chat_picture)

    session.add(new_chat)
    await session.commit()

    usernames = [creator_username, chat_in.companion_username]
    passwords = [chat_in.creator_chat_password, chat_in.companion_chat_password]
    for username, password in zip(usernames, passwords):
        stmt = select(User).filter(User.username == username)
        result: Result = await session.execute(stmt)
        user_id = result.scalar().id

        new_user_chat = UserChatAssociation(
            user_id=user_id, chat_id=new_chat.id, password=password
        )
        session.add(new_user_chat)
    await session.commit()

    return ChatResponse(
        name=chat_in.name,
        chat_picture=chat_in.chat_picture,
        created_at=datetime.utcnow(),
        password=chat_in.creator_chat_password,
    )


async def get_chats(session: AsyncSession, username: str) -> list[ChatResponse]:
    stmt = (
        select(User)
        .options(selectinload(User.chats_details).joinedload(UserChatAssociation.chat))
        .where(User.username == username)
    )

    user = (await session.scalars(stmt)).first()
    chats: list[ChatResponse] = []
    if user:
        for chat_user_details in user.chats_details:  # type: UserChatAssociation

            chat = ChatResponse(
                name=chat_user_details.chat.name,
                chat_picture=chat_user_details.chat.chat_picture,
                created_at=chat_user_details.chat.created_at,
                password=chat_user_details.password,
            )
            chats.append(chat)
    return chats

    # # chat = Chat(name="name1", chat_picture=b"")
    # # session.add(chat)
    # # await session.commit()
    # stmt = select(Chat).order_by(Chat.id)
    # result: Result = await session.execute(stmt)
    # chats = result.scalars().all()
    # return list(chats)

    # stmt = select(Chat).options(selectinload(Chat.users_details))
    # chats = await session.scalars(stmt)
    # print(chats)
    # for chat in chats:
    #     print(chat.id, chat.name)
    #     for user in chat.users_details:
    #         print(user.id, user.username)
    #
    # return list(chats)

    # stmt = select(Chat)
    #
    # result: Result = await session.execute(stmt)

    # print("hello")

    # chats = result.scalars().all()
    # return [ChatResponse(name="", password="", chat_picture=b"", created_at=func.now())]
