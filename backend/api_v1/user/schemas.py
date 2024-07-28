from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    # model_config = ConfigDict(strict=True)
    username: str
    profile_picture: bytes
    first_name: str
    last_name: str
    password_hash: bytes
    public_key: str
    enc_private_key: str


class UserCreate(UserBase):
    username: str
    profile_picture: str
    first_name: str
    last_name: str
    password_hash: str
    public_key: str
    enc_private_key: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    username: str | None = None
    profile_picture: bytes | None = None
    first_name: str | None = None
    last_name: str | None = None
    password_hash: bytes | None = None
    public_key: str | None = None
    enc_private_key: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
