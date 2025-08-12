from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from lib.database.db import get_session
from lib.entities.users.model import User
from lib.entities.books.model import Book
from lib.entities.wishlist.model import Wishlist
from lib.entities.books.schema import BookResponseSchema
from lib.core.security import get_current_user, get_password_hash

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/{id}")
def add_to_wishlist(db: T_Session, user: CurrentUser, id: int):
    db_book = db.scalar(select(Book).where(
        Book.id == id, Book.user_id == user.id))

    if not db_book:
        raise HTTPException(404, "Book not found.")

    db_book_wishlist = db.scalar(
        select(Wishlist).where(Wishlist.user_id == user.id, Wishlist.book_id == id))

    if db_book_wishlist:
        raise HTTPException(409, "Book already in wishlist.")

    wishlit_item = Wishlist(user_id=user.id, book_id=id)

    db.add(wishlit_item)
    db.commit()
    db.refresh(wishlit_item)


@router.get("", status_code=200, response_model=list[BookResponseSchema])
def get_wishlist(db: T_Session, user: CurrentUser):
    books_in_wishlist = db.scalars(
        select(Book)
        .join(Wishlist)
        .where(Wishlist.user_id == user.id)
    ).all()

    return books_in_wishlist


@router.delete("/{id}", status_code=204)
def remove_from_wishlist(db: T_Session, user: CurrentUser, id: int):
    wishlist_item = db.scalar(select(Wishlist).where(
        Wishlist.book_id == id, Wishlist.user_id == user.id))

    if not wishlist_item:
        raise HTTPException(404, "Book not in wishlist.")

    db.delete(wishlist_item)
    db.commit()
