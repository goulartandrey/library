from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class BaseParams(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = 10
