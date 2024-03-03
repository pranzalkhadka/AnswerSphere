from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str


# Schema for the request of create post
class PostCreate(PostBase):
    pass


# Schema for the request of update post
class PostUpdate(PostBase):
    pass


# Schema for the response of the user credentials
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# Schema for the response of the post
class PostResponse(BaseModel):
    title: str
    content: str
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


# Schema for the request of the user credentials
class UserCreate(BaseModel):
    email: EmailStr
    password: str



# Schema for the request of the user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for the response of the user login
class Token(BaseModel):
    access_token: str
    token_type: str



# Schema for the token data
class TokenData(BaseModel):
    id: Optional[str] = None

