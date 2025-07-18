from passlib.context import CryptContext

from jose import jwt, JWTError
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC
import os

load_dotenv(dotenv_path=Path(__name__).resolve().parent / ".env")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180
REFRESH_TOKEN_EXPIRE_MINUTES = 42600


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expires_delta: float | None = None):
    """
    - Creates a new JWT token for logging-in user
    """

    delta = (
        timedelta(minutes=expires_delta)
        if expires_delta
        else timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expire_time = datetime.now(UTC) + delta
    data.update({"exp": expire_time})

    # data = {"username": <>, "password": <>, "role": <>, "exp": <>}

    jwt_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return jwt_token