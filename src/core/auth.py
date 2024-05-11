from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from pytz import timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from pydantic import BaseModel

import os
from typing import Optional
from datetime import datetime, timedelta

from src.core.database import Session
from src.core.deps import get_session
from src.models import User
from src.core.security import verify_password

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60 * 24 * 30)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'/api/v1'
)


class TokenData(BaseModel):
    email: Optional[str] = None


async def authenticate_user(email: str, password: str, db: AsyncSession) -> Optional[User]:
    async with db as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if not user:
            return None
        if not verify_password(password, user.password):
            return None

        return user


def _create_token(token_type: str, expires_delta: timedelta, sub: str) -> str:
    payload = {}
    tz = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=tz) + expires_delta

    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz=tz)
    payload["sub"] = str(sub)

    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(sub: str) -> str:
    return _create_token(token_type="access_token", expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES, sub=sub)


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(User).filter(User.id == int(token_data.email))
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()
        if user is None:
            raise credentials_exception

        return user
