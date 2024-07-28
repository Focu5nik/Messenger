from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, LargeBinary

if TYPE_CHECKING:
    from .user_chat_association import UserChatAssociation


class User(Base):
    profile_picture: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32), default="", server_default="")
    last_name: Mapped[str] = mapped_column(String(32), default="", server_default="")
    password_hash: Mapped[bytes] = mapped_column(default="", server_default="")
    public_key: Mapped[str] = mapped_column(default="", server_default="")
    enc_private_key: Mapped[str] = mapped_column(default="", server_default="")

    chats_details: Mapped[list["UserChatAssociation"]] = relationship(
        back_populates="user"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
