from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud

from .dependencies import user_by_username
from .schemas import User, UserCreate, UserUpdate, UserUpdatePartial
from api_v1.jwt_auth.jwt_auth import get_current_token_payload


router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{username}/", response_model=User)
async def get_user(
    user: User = Depends(user_by_username),
    payload: dict = Depends(get_current_token_payload),
):
    return user


@router.put("/{username}/")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_username),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/{username}/")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_username),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


@router.delete("/{username}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_username),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_user(session=session, user=user)
