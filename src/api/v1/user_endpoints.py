from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models import User
from src.schemas import UserSchema, LoginSchema, UserCreateSchema
from src.core.deps import get_session
from src.core.auth import get_current_user, authenticate_user, create_access_token
from src.core.security import get_password_hash

router = APIRouter()


@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """
    Retrieves a user by their ID.

    :param user_id: The ID of the user to retrieve.
    :param db: The database session.
    :return: A User object if found, otherwise raises an HTTPException.
    """
    async with db as session:
        note = await session.get(User, user_id)

        if note is None:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)

        return note


@router.get("/user", response_model=UserSchema)
def get_logged_user(current_user: User = Depends(get_current_user)):
    """
        Retrieves the currently logged-in user.

        :param current_user: The current user object.
        :return: The current user object.
    """
    return current_user


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    """
        Registers a new user.

        :param user: A UserCreateSchema object containing the new user's information.
        :param db: The database session.
        :return: A User object if the user is successfully registered.
    """
    user.password = get_password_hash(user.password)
    new_user = User(**user.dict())

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            raise HTTPException(detail='Email already exists', status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return new_user


@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_session)):
    """
        Authenticates a user and returns an access token.

        :param data: A LoginSchema object containing the user's email and password.
        :param db: The database session.
        :return: A JSONResponse containing the access token and token type.
    """
    user = await authenticate_user(data.email, data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect data access")

    return JSONResponse(content={"access_token": create_access_token(sub=user.id), "token_type": "bearer"})
