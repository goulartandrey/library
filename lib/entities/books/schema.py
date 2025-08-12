from typing import Optional
from pydantic import BaseModel

from lib.entities._base.schema import BaseParams


class BookResponseSchema(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    description: str


class CreateBookSchema(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    description: str


class BooksQuerySchema(BaseParams):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
