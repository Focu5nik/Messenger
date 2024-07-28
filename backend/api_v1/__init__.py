from fastapi import APIRouter
from .user.views import router as user_router

from .chat.views import router as chat_router
from .message.views import router as message_router
from .jwt_auth.jwt_auth import router as jwt_auth_router

router = APIRouter()
router.include_router(router=user_router, prefix="/users")
router.include_router(router=jwt_auth_router, prefix="/jwt_auth")
router.include_router(router=chat_router, prefix="/chats")
router.include_router(router=message_router, prefix="/messages")
