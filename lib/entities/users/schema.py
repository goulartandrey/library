from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
