from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError

from typing import Annotated

from app.db import SessionLocal
from app.utils import SECRET_KEY, ALGORITHM
from app.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]


def get_current_user(
    request: Request,
    db: db_dep
):
    auth_header = request.headers.get("Authorization")
    is_bearer = auth_header.startswith("Bearer ") if auth_header else False
    token = auth_header.split(" ")[1] if auth_header else ""

    if not auth_header and is_bearer:
        raise HTTPException(
            status_code=401,
            detail="You are not authenticated."
        )


    try:
        decoded_jwt = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        print(decoded_jwt)
        user_id = decoded_jwt.get("user_id")

        db_user = db.query(User).filter(User.id == user_id).first()

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    return db_user

current_user_dep = Annotated[User, Depends(get_current_user)]