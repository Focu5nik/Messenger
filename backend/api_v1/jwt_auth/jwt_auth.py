from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    # HTTPBearer,
    # HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel, EmailStr, ConfigDict

from auth import utils as auth_utils

from api_v1.user.schemas import User
from core.models import db_helper
from api_v1.user import crud

# from users.schemas import UserSchema


router = APIRouter(prefix="/jwt", tags=["JWT"])


# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt_auth/jwt/login/",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


# Give token to user


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await crud.get_user(session=session, username=username)

    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password_hash,
    ):
        raise unauthed_exc

    return user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        "first_name": user.first_name,
        # "logged_in_at"
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


# Get info of user by token


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


#
# async def get_current_auth_user(
#     payload: dict = Depends(get_current_token_payload),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> User:
#     username: str | None = payload.get("sub")
#
#     user = await crud.get_user(session=session, username=username)
#     if user:
#         return user
#
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="token invalid (user not found)",
#     )
#
#
# @router.get("/users/me/")
# def auth_user_check_self_info(
#     payload: dict = Depends(get_current_token_payload),
#     user: User = Depends(get_current_auth_user),
# ):
#     iat = payload.get("iat")
#     return {
#         "username": user.username,
#         "first_name": user.first_name,
#         "logged_in_at": iat,
#     }
