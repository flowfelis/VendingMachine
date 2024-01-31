from typing import Annotated

import bcrypt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db


def hash_password(plain_password):
    """
    Hash a password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str.encode(plain_password), salt)

    return hashed


def compare_passwords(
        incoming_plain_password,
        current_hashed_password
):
    """
    compare passwords
    and return a boolean value
    """
    return bcrypt.checkpw(
        str.encode(incoming_plain_password),
        current_hashed_password
    )


basic_auth = HTTPBasic()


def authenticate(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        db: Session = Depends(get_db)
):
    # authenticate username
    db_user = crud.get_user_by_username(db, credentials.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # authenticate password
    is_correct_password = compare_passwords(
        credentials.password,
        db_user.hashed_password
    )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return db_user.id
