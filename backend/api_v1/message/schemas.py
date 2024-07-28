from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    body: str
    sender_user_id: int
    chat_id: int
    created_at: datetime


class MessageSchema(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MessageCreate(BaseModel):
    body: str
    chat_id: int


class MessageResponse(MessageBase):
    pass
