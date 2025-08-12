from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from lib.database.db import get_session
from lib.entities.users.model import User
from lib.entities.users.schema import UserResponseSchema, CreateUserSchema
from lib.core.security import get_current_user, get_password_hash


router = APIRouter(prefix="/users", tags=["users"])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=List[UserResponseSchema])
def get_users(db: T_Session, user: CurrentUser):
    db_users = db.scalars(select(User).where(User.id == user.id)).all()

    return db_users


@router.post("", response_model=UserResponseSchema)
def create_user(db: T_Session, payload: CreateUserSchema):
    db_user = db.scalar(select(User).where(
        (User.username == payload.username) | (User.email == payload.email)))

    if db_user:
        raise HTTPException(409, 'Username or email already exists')

    user = User(username=payload.username,
                email=payload.email, password=get_password_hash(payload.password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{id}", status_code=200, response_model=UserResponseSchema)
def update_user(db: T_Session, user: CurrentUser, payload: CreateUserSchema, id: int):
    if user.id != id:
        raise HTTPException(403, "Not enough permission.")

    user.username = payload.username
    user.email = payload.email
    user.password = get_password_hash(payload.password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )


@router.delete("/{id}", status_code=204)
def delete_user(db: T_Session, user: CurrentUser, id: int):
    if user.id != id:
        raise HTTPException(403, "Not enough permission.")
    db.delete(user)
    db.commit()
