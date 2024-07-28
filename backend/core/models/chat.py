from datetime import datetime

from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, String, LargeBinary

if TYPE_CHECKING:
    from .user_chat_association import UserChatAssociation
    from .message import Message


class Chat(Base):
    name: Mapped[str] = mapped_column(String(32), unique=False)
    chat_picture: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    users_details: Mapped[list["UserChatAssociation"]] = relationship(
        back_populates="chat"
    )

    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
