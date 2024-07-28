from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, func

if TYPE_CHECKING:
    from .user import User
    from .chat import Chat


class UserChatAssociation(Base):
    __tablename__ = "user_chat_association"
    __table__args__ = (
        UniqueConstraint(
            "user_id",
            "chat_id",
            name="idx_unique_user_chat",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    password: Mapped[str] = mapped_column(default="", server_default="")

    # association between Association -> User
    user: Mapped["User"] = relationship(
        back_populates="chats_details",
    )

    # association between Association -> Chat
    chat: Mapped["Chat"] = relationship(
        back_populates="users_details",
    )
