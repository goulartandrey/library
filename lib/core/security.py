from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from lib.database.db import get_session
from lib.entities.users.model import User
from lib.core.settings import Settings

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + \
        timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, Settings().SECRET_KEY,
                         algorithm=Settings().ALGORITHM)

    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        401, "Could not validate credentials", headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = decode(token, Settings().SECRET_KEY,
                         algorithms=Settings().ALGORITHM)
        subject = payload.get('sub')
        if not subject:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = db.scalar(select(User).where(
        (User.username == subject) | (User.email == subject)))

    if not user:
        raise credentials_exception

    return user
