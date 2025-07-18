from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.models import User
from app.schemas.auth import UserRegisterIn, UserRegisterOut, UserLoginOut
from app.utils import (
    hash_password,
    verify_password,
    create_jwt_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register/", response_model=UserRegisterOut)
async def register(db: db_dep, user_in: UserRegisterIn):
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        username=user_in.email
    )

    is_user_exists = db.query(User).count()

    if not is_user_exists:
        new_user.is_admin = True

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login/", response_model=UserLoginOut)
async def login(db: db_dep, user_in: UserRegisterIn):
    # If user exists in database
    # If passwords match
    # Return access token

    user = db.query(User).filter(User.email == user_in.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=403,
            detail="Invalid credentials."
        )

    access_token = create_jwt_token(
        data={
            "user_id": user.id
        },
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_jwt_token(
        data={
            "user_id": user.id
        },
        expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


@router.post("/refresh/")
async def get_refresh_token():
    pass


@router.get("/profile", response_model=UserRegisterOut)
async def get_profile(current_user: current_user_dep):
    return current_user