from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from lib.database.db import get_session
from lib.core.security import get_current_user
from lib.entities.books.model import Book
from lib.entities.books.schema import BookResponseSchema, BooksQuerySchema, CreateBookSchema
from lib.entities.users.model import User

router = APIRouter(prefix="/books", tags=["books"])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[BookResponseSchema])
def get_books(db: T_Session, user: CurrentUser, query: BooksQuerySchema = Depends()):
    db_query = select(Book).where(Book.user_id == user.id)

    if query.title:
        db_query = db_query.filter(Book.title.contains(query.title))
    if query.author:
        db_query = db_query.filter(Book.author.contains(query.author))
    if query.year:
        db_query = db_query.filter(Book.year.contains(query.year))

    books = db.scalars(db_query.offset(query.offset).limit(query.limit)).all()

    return books


@router.get("/{id}", response_model=BookResponseSchema)
def get_book(db: T_Session, user: CurrentUser, id: int):
    db_book = db.scalar(select(Book).where(
        Book.id == id, Book.user_id == user.id))

    if not db_book:
        raise HTTPException(404, 'Book not found.')

    return db_book


@router.post("", response_model=BookResponseSchema)
def create_book(db: T_Session, user: CurrentUser, payload: CreateBookSchema):
    db_book = db.scalar(select(Book).where(
        Book.title == payload.title, Book.author == payload.author))
    if db_book:
        raise HTTPException(409, "Livro já cadastrado.")

    new_book = Book(**payload.model_dump(), user_id=user.id)

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.put("/{id}", status_code=200, response_model=BookResponseSchema)
def update_book(db: T_Session, user: CurrentUser, payload: CreateBookSchema, id: int):
    db_book = db.scalar(select(Book).where(
        Book.id == id, Book.user_id == user.id))

    if not db_book:
        raise HTTPException(404, 'Book not found.')

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.delete("/{id}", status_code=204)
def delete_book(db: T_Session, user: CurrentUser, id: int):
    db_book = db.scalar(select(Book).where(
        Book.id == id, Book.user_id == user.id))

    if not db_book:
        raise HTTPException(404, 'Book not found.')

    db.delete(db_book)
    db.commit()
