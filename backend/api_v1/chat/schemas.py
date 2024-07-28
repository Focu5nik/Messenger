from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatBase(BaseModel):
    name: str
    chat_picture: bytes
    created_at: datetime


class ChatResponse(ChatBase):
    password: str
    # companion_username: str


class ChatSchema(ChatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ChatCreate(BaseModel):
    name: str
    chat_picture: bytes
    companion_username: str
    creator_chat_password: str
    companion_chat_password: str
