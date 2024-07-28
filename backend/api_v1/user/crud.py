from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from core.models import User
from auth import utils as auth_utils

from .schemas import UserCreate, UserUpdate, UserUpdatePartial


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, username: str) -> User | None:
    # return await session.get(User, user_id)
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    return user


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    # user = User(**user_in.model_dump())
    # session.add(user)
    # await session.commit()
    # # await session.refresh(User)
    # return user
    stmt = select(User).filter(User.username == user_in.username)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username {user_in.username} is alredy taken!",
        )

    user_data = user_in.model_dump()
    user_data["password_hash"] = auth_utils.hash_password(user_in.password_hash)
    user_data["profile_picture"] = user_in.profile_picture.encode()
    user = User(**user_data)
    session.add(user)
    await session.commit()
    # await session.refresh(User)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
