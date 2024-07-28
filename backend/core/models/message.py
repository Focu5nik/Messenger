from typing import TYPE_CHECKING

from .base import Base
from datetime import datetime
from sqlalchemy import func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .chat import Chat


class Message(Base):
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    sender_user_id: Mapped[int] = mapped_column(nullable=False)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    chat: Mapped["Chat"] = relationship(back_populates="messages")
