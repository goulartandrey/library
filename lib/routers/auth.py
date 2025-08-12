from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from lib.database.db import get_session
from lib.entities.users.model import User
from lib.entities._base.schema import TokenSchema
from lib.core.security import get_current_user, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=['auth'])


T_Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/token", response_model=TokenSchema)
def login_for_access_token(
    db: T_Session,
    form_data: OAuth2Form
):
    db_user = db.scalar(select(User).where(
        User.username == form_data.username))

    if not db_user:
        raise HTTPException(401,
                            "Incorret username or password")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(401,
                            "Incorret username or password")

    access_token = create_access_token(
        {'sub': db_user.email}
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post("/refresh_token", response_model=TokenSchema)
def refresh_access_token(db: T_Session, user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
